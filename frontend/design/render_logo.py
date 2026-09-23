"""Render the user-supplied octagon FBX as a lightweight header turntable."""
import math
from pathlib import Path
import bpy
from mathutils import Vector

source = Path('/Users/mehtabghuman/Downloads/mma-octagon')
output = Path('/tmp/octagon-logo')
output.mkdir(exist_ok=True)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
bpy.ops.import_scene.fbx(filepath=str(source / 'source/octagon Sketch.fbx'))
scene = bpy.context.scene
objects = list(scene.objects)
for img in bpy.data.images:
    filename = Path(img.filepath).name
    replacements = {'GWC Metal Fencing_Normal.jpg': 'GWC Metal Fencing_Normal.jpeg', 'UFC 238 Canvas.jpg': 'UFC 238 Canvas.jpeg'}
    path = source / 'textures' / replacements.get(filename, filename)
    if path.exists():
        img.filepath = str(path)
        img.reload()
        img.pack()
points = [obj.matrix_world @ Vector(corner) for obj in objects if obj.type == 'MESH' for corner in obj.bound_box]
center = Vector(tuple((min(p[i] for p in points) + max(p[i] for p in points))/2 for i in range(3)))
root = bpy.data.objects.new('Octagon turntable', None)
scene.collection.objects.link(root)
for obj in objects:
    obj.location -= center
    obj.parent = root
root.rotation_euler.z = 0
root.keyframe_insert(data_path='rotation_euler', frame=1)
root.rotation_euler.z = math.tau
root.keyframe_insert(data_path='rotation_euler', frame=121)
for layer in root.animation_data.action.layers:
    for strip in layer.strips:
        for bag in strip.channelbags:
            for curve in bag.fcurves:
                for key in curve.keyframe_points:
                    key.interpolation = 'LINEAR'
scene.render.engine = 'CYCLES'
scene.cycles.samples = 8
scene.cycles.use_denoising = True
scene.render.resolution_x = 320
scene.render.resolution_y = 224
scene.render.resolution_percentage = 100
scene.render.fps = 24
scene.frame_start, scene.frame_end = 1, 120
scene.world.use_nodes = True
scene.world.node_tree.nodes['Background'].inputs['Color'].default_value = (1,1,1,1)
scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value = 1
scene.render.film_transparent = False
scene.view_settings.view_transform = 'Standard'
for loc, energy, size in [((2,-8,14),1800,10),((-9,3,8),1200,8)]:
    data = bpy.data.lights.new('Softbox','AREA')
    data.energy, data.size = energy, size
    light = bpy.data.objects.new('Softbox',data)
    scene.collection.objects.link(light)
    light.location = loc
    light.rotation_euler = (-light.location).to_track_quat('-Z','Y').to_euler()
data = bpy.data.cameras.new('Logo camera')
data.type = 'ORTHO'
data.ortho_scale = 18.7
camera = bpy.data.objects.new('Logo camera',data)
scene.collection.objects.link(camera)
camera.location = (18,-22,24)
camera.rotation_euler = (-camera.location).to_track_quat('-Z','Y').to_euler()
scene.camera = camera
scene.render.image_settings.file_format = 'PNG'
scene.render.filepath = str(output / 'frame_')
scene.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=str(Path(__file__).with_name('octagon-logo.blend')))
bpy.ops.render.render(animation=True)
