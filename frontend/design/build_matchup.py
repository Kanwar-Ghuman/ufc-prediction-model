"""Build photo-referenced Van/Pantoja models and a looping exchange in Blender."""
import math
from pathlib import Path
import bpy
from mathutils import Vector

ROOT = Path('/Users/mehtabghuman/Desktop/UFC_Prediction')
IMAGES = ROOT / 'model/data/fighter_images'
OUT = ROOT / 'frontend/design/van-pantoja.blend'
scene = bpy.data.scenes.new('Van vs Pantoja')
bpy.context.window.scene = scene
scene.render.engine = 'CYCLES'
scene.cycles.samples = 24
scene.cycles.use_denoising = True
scene.render.resolution_x = 960
scene.render.resolution_y = 600
scene.render.resolution_percentage = 100
scene.render.fps = 24
scene.frame_start, scene.frame_end = 1, 120
scene.render.image_settings.file_format = 'PNG'
scene.render.filepath = '/private/tmp/van-pantoja/frame_'
Path('/private/tmp/van-pantoja').mkdir(exist_ok=True)
world = bpy.data.worlds.new('Matchup studio'); world.use_nodes = True; scene.world = world
bg = next(n for n in world.node_tree.nodes if n.type == 'BACKGROUND')
bg.inputs['Color'].default_value = (.85,.88,1,1); bg.inputs['Strength'].default_value = .35

def material(name, color, rough=.55, image=None):
    m = bpy.data.materials.new(name); m.use_nodes = True
    n = next(n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')
    n.inputs['Base Color'].default_value = (*color,1)
    n.inputs['Roughness'].default_value = rough
    if image:
        tex = m.node_tree.nodes.new('ShaderNodeTexImage')
        tex.image = bpy.data.images.load(str(IMAGES / image), check_existing=True)
        tex.extension = 'EXTEND'
        m.node_tree.links.new(tex.outputs['Color'], n.inputs['Base Color'])
    return m

black = material('MMA glove leather',(.012,.014,.015),.34)
gold = material('Van gold trim',(.58,.34,.075),.42)
red = material('Pantoja oxblood trunks',(.22,.015,.018))
white = material('Canvas and lettering',(.82,.82,.79))
blue = material('Blue corner tape',(.035,.10,.27))
redtape = material('Red corner tape',(.55,.025,.025))
hair = material('Short dark hair',(.018,.012,.009),.85)


def empty(name, parent=None):
    o=bpy.data.objects.new(name,None); scene.collection.objects.link(o); o.parent=parent; return o


def ball(name, pos, scale, mat, parent=None):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32,ring_count=20)
    o=bpy.context.object; o.name=name; o.parent=parent; o.location=pos; o.scale=scale
    o.data.materials.append(mat)
    for p in o.data.polygons:p.use_smooth=True
    return o


def mesh(name, verts, faces, materials, uvs=None, indices=None, parent=None):
    data=bpy.data.meshes.new(name); data.from_pydata(verts,[],faces); data.update()
    obj=bpy.data.objects.new(name,data); scene.collection.objects.link(obj); obj.parent=parent
    for m in materials:data.materials.append(m)
    if uvs:
        uv=data.uv_layers.new()
        for poly in data.polygons:
            for loop in poly.loop_indices:uv.data[loop].uv=uvs[data.loops[loop].vertex_index]
    for i,p in enumerate(data.polygons):
        p.use_smooth=True
        if indices:p.material_index=indices[i]
    return obj


def torso(name, skin, photo, parent):
    rings=[(.87,.13,.085),(.94,.139,.088),(1.03,.14,.092),(1.13,.168,.105),(1.23,.205,.12),(1.31,.216,.108),(1.36,.185,.075),(1.41,.075,.065)]
    verts=[];uvs=[];faces=[];indices=[]; N=48
    for z,w,depth in rings:
        for j in range(N):
            a=2*math.pi*j/N; x=w*math.sin(a); y=-depth*math.cos(a)
            verts.append((x,y,z))
            if name=='Pantoja':u=(220+x/.22*140)/440; v=1-(570-(z-.87)/.54*335)/700
            else:u=(282+max(0,x)/.21*68)/467;v=1-(420-(z-1.03)/.36*170)/700
            uvs.append((u,v))
    for i in range(len(rings)-1):
        for j in range(N):
            faces.append((i*N+j,i*N+(j+1)%N,(i+1)*N+(j+1)%N,(i+1)*N+j))
            front=math.cos(2*math.pi*(j+.5)/N)>.6
            tattoo=name=='Pantoja' or (verts[i*N+j][0]>.028 and 1.03<=rings[i][0]<=1.36)
            indices.append(int(front and tattoo))
    return mesh(name+' anatomical torso',verts,faces,[skin,photo],uvs,indices,parent)


def head(name, skin, photo, parent):
    # Anatomical horizontal loops; the face is a curved, photo-textured surface.
    rings=[(-.128,.034,.036),(-.115,.052,.051),(-.09,.071,.065),(-.06,.081,.075),(-.025,.086,.083),(.012,.089,.089),(.045,.087,.089),(.08,.08,.079),(.109,.066,.06),(.128,.04,.036),(.137,.004,.004)]
    verts=[];uvs=[];faces=[];indices=[];N=64
    for z,w,depth in rings:
        for j in range(N):
            a=2*math.pi*j/N;x=w*math.sin(a);front=max(0,math.cos(a));y=-depth*math.cos(a)
            nose=.023*math.exp(-(x/.022)**2-((z+.015)/.036)**2)
            brow=.006*math.exp(-((z-.033)/.012)**2)
            y-=(nose+brow)*front**12
            verts.append((x,y,z))
            center,half,top,bottom=(263,80,26,238) if name=='Van' else (250,73,7,214)
            uvs.append(((center+x/.09*half)/520,1-(top+(.137-z)/.265*(bottom-top))/325))
    for i in range(len(rings)-1):
        for j in range(N):
            faces.append((i*N+j,i*N+(j+1)%N,(i+1)*N+(j+1)%N,(i+1)*N+j))
            indices.append(int(math.cos(2*math.pi*(j+.5)/N)>.12))
    h=mesh(name+' photo sculpt head',verts,faces,[skin,photo],uvs,indices,parent)
    for x in [-.09,.09]:ball(name+' ear',(x,.005,-.017),(.014,.02,.034),skin,parent)
    # Hair is modeled on the back and crown; the front hairline comes from the photo.
    cap=ball(name+' cropped hair',(0,.017,.077),(.083,.076,.063 if name=='Van' else .045),hair,parent)
    return h


def link(o,a,b,r1,r2=None):
    a,b=Vector(a),Vector(b); o.location=(a+b)*.5
    o.rotation_mode='QUATERNION';o.rotation_quaternion=(b-a).to_track_quat('Z','Y')
    o.scale=(r1,r2 or r1,(b-a).length*.61)


def label(text, pos, size, mat, parent, rotation=(math.pi/2,0,0)):
    c=bpy.data.curves.new(text,'FONT');c.body=text;c.size=size;c.align_x='CENTER';c.extrude=.0002
    o=bpy.data.objects.new(text,c);scene.collection.objects.link(o);o.parent=parent;o.location=pos;o.rotation_euler=rotation;c.materials.append(mat);return o

fighters=[]
for name,slug,x,angle in [('Van','joshua-van',-.56,.72),('Pantoja','alexandre-pantoja',.56,-.72)]:
    skin=material(name+' skin',(.42,.215,.125) if name=='Van' else (.48,.26,.16),.58)
    face=material(name+' face reference',(1,1,1),.72,slug+'-head.png')
    bodyphoto=material(name+' body reference',(1,1,1),.67,slug+'.png')
    root=empty(name+' footwork');root.location=(x,0,0);root.rotation_euler.z=angle
    upper=empty(name+' torso pivot',root)
    torso(name,skin,bodyphoto,upper)
    ball(name+' neck',(0,.015,1.416),(.065,.063,.087),skin,upper)
    hp=empty(name+' head pivot',upper);hp.location=(0,-.005,1.565);head(name,skin,face,hp)
    # Tailored shorts with a waistband and separate leg openings.
    trunkmat=black if name=='Van' else red
    ball(name+' trunks pelvis',(0,0,.835),(.157,.104,.112),trunkmat,root)
    for s in [-1,1]:ball(name+' trunks leg',(s*.085,-.018,.757),(.092,.11,.11),trunkmat,root)
    ball(name+' waistband',(0,-.003,.914),(.148,.1,.026),black,root)
    label(name.upper(),(0,-.106,.894),.024,gold if name=='Van' else white,root)
    for s in [-1,1]:
        ball(name+' shorts side trim',(s*.15,-.026,.81),(.009,.078,.099),gold if name=='Van' else white,root)
    parts={}
    for lr in ['l','r']:
        for seg,r in [('upperarm',.064),('forearm',.049),('thigh',.095),('shin',.062)]:
            parts[lr+seg]=ball(name+' '+lr+seg,(0,0,0),(r,r,.1),skin,root)
        for joint,r in [('shoulder',.077),('elbow',.046),('knee',.063)]:
            parts[lr+joint]=ball(name+' '+lr+joint,(0,0,0),(r,r,r),skin,root)
        foot=empty(name+' '+lr+' foot',root);parts[lr+'foot']=foot
        ball(name+' foot instep',(0,-.037,.027),(.045,.095,.04),skin,foot)
        for toe in range(5):ball(name+' toe',((toe-2)*.016,-.11+(abs(toe-1)*.004),.015),(.012,.026,.015),skin,foot)
        glove=empty(name+' '+lr+' MMA glove',root);parts[lr+'glove']=glove
        ball(name+' glove',(0,-.006,0),(.061,.043,.065),black,glove)
        ball(name+' wrist tape',(0,.015,-.067),(.045,.037,.023),redtape if name=='Van' else blue,glove)
        for k in range(4):ball(name+' exposed knuckle',((k-1.5)*.024,-.027,.048),(.014,.025,.022),skin,glove)
        ball(name+' thumb',(.061,-.015,-.009),(.024,.025,.04),skin,glove)
        label('MMA',(0,-.05,-.005),.018,white,glove)
    fighters.append((name,root,upper,hp,parts,x,angle))


def pulse(t,c,w):return math.exp(-((t-c)/w)**2)
for frame in range(1,122,2):
    t=(frame-1)/120
    for name,root,upper,hp,p,x,angle in fighters:
        van=name=='Van'; jab=pulse(t,.23 if van else .65,.055);cross=pulse(t,.42 if van else .80,.055)
        duck=pulse(t,.66 if van else .42,.07)
        bob=.008*math.sin(t*math.tau*3)
        root.location=(x+(.065 if van else -.065)*(jab+cross),.018*math.sin(t*math.tau),0)
        root.rotation_euler.z=angle+(.10 if van else -.10)*cross
        upper.location=(0,.015*duck,-.052*duck+bob)
        upper.rotation_euler.x=.05*duck
        hp.rotation_euler=(.035*math.sin(t*math.tau),.07*duck,(-.08 if van else .08)*cross)
        for lr,s in [('l',-1),('r',1)]:
            lead=lr=='l';ext=jab if lead else cross
            shoulder=(s*.202,.005,1.31-.05*duck+bob)
            elbow=(s*(.24-.10*ext),-.075-.29*ext,1.12+.24*ext-.04*duck+bob)
            hand=(s*(.12-.09*ext),-.21-.43*ext,1.46-.012*ext-.04*duck+bob)
            link(p[lr+'upperarm'],shoulder,elbow,.065,.062);link(p[lr+'forearm'],elbow,hand,.049,.046)
            p[lr+'shoulder'].location=shoulder;p[lr+'elbow'].location=elbow
            p[lr+'glove'].location=hand;p[lr+'glove'].rotation_euler=(.12+ext*1.20,0,s*.12)
            hip=(s*.082,0,.82);knee=(s*.117,-.12 if lead else .115,.46)
            ankle=(s*.16,-.23 if lead else .25,.065)
            link(p[lr+'thigh'],hip,knee,.095,.092);link(p[lr+'shin'],knee,ankle,.06,.053)
            p[lr+'knee'].location=knee;p[lr+'foot'].location=ankle
        for obj in [root,upper,hp,*p.values()]:
            obj.keyframe_insert(data_path='location',frame=frame)
            obj.keyframe_insert(data_path='rotation_euler',frame=frame)
            obj.keyframe_insert(data_path='rotation_quaternion',frame=frame)
            obj.keyframe_insert(data_path='scale',frame=frame)

bpy.ops.mesh.primitive_plane_add(size=200)
floor=bpy.context.object;floor.name='White studio floor';floor.data.materials.append(white)
# Fine octagonal canvas outline.
curve=bpy.data.curves.new('Octagon outline','CURVE');curve.dimensions='3D';curve.bevel_depth=.006;curve.bevel_resolution=2
spline=curve.splines.new('POLY');spline.points.add(8)
for i,p in enumerate(spline.points):a=math.tau*i/8;p.co=(1.8*math.cos(a),1.8*math.sin(a),.002,1)
outline=bpy.data.objects.new('Octagon outline',curve);scene.collection.objects.link(outline);curve.materials.append(material('Canvas outline',(.42,.43,.42)))
for loc,energy,size in [((-2,-4,5),400,4),((3,-1,3),230,3),((0,3,4),500,3)]:
    data=bpy.data.lights.new('Studio softbox','AREA');data.energy=energy;data.size=size
    o=bpy.data.objects.new('Studio softbox',data);scene.collection.objects.link(o);o.location=loc;o.rotation_euler=(Vector((0,0,1))-o.location).to_track_quat('-Z','Y').to_euler()
data=bpy.data.cameras.new('Matchup camera');data.type='ORTHO';data.ortho_scale=2.9
cam=bpy.data.objects.new('Matchup camera',data);scene.collection.objects.link(cam);cam.location=(0,-6,2.8);cam.rotation_euler=(Vector((0,0,.90))-cam.location).to_track_quat('-Z','Y').to_euler();scene.camera=cam
scene.frame_set(1)
for image in bpy.data.images:
    if image.source=='FILE' and image.has_data:image.pack()
bpy.ops.wm.save_as_mainfile(filepath=str(OUT),copy=True)
print('Saved',OUT,'with',len(scene.objects),'objects')
