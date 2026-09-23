# Octagon visual direction

A white sports editorial interface: real fighter photography, fine rules,
compact probability bars, charcoal type, and one restrained red accent.
Matchups lead; method/round distributions and research remain in expandable
details. Three columns become two at 1000px and one at 640px. External font
requests, gradients, glass panels, and glowing borders are removed.

## Research

- [NN/g: Characteristics of Minimalism](https://www.nngroup.com/articles/characteristics-minimalism/)
  supports limited color, purposeful whitespace, and typography as hierarchy.
  Removing useful information indiscriminately is not the objective.
- [NN/g: Visual Hierarchy](https://www.nngroup.com/articles/visual-hierarchy-ux-definition/)
  informs the priority of fighter identity, then probabilities, then detail.
- [Joshua Snoddy: Why AI Websites Look the Same](https://www.joshuasnoddy.com/blog/why-ai-websites-look-the-same/)
  discusses repeated gradient/glass/card defaults. This is qualitative design
  commentary, not a scientific test of whether a site was AI generated.

## Motion

`sparring-study.blend` contains a separate `Octagon - Sparring study` scene.
The original scene is preserved. Two original sculptural figures exchange jabs
and slips over 72 frames at 24 fps. These illustrate movement; they are not
fighter likenesses or simulations of predicted outcomes.

The site uses a 720 × 450 H.264 video and JPEG poster in `public/motion/`.
Reduced-motion preferences disable automatic playback. The visible control
lets the viewer play or pause. No 3D library is required at runtime.

Render from the frontend directory with Blender and FFmpeg installed:

```sh
mkdir -p /tmp/octagon-frames
blender -b design/sparring-study.blend -S 'Octagon - Sparring study' -o /tmp/octagon-frames/frame_ -a
ffmpeg -framerate 24 -i /tmp/octagon-frames/frame_%04d.png -c:v libx264 -crf 23 -pix_fmt yuv420p -movflags +faststart public/motion/sparring-study.mp4
```

Portraits remain in the backend cache with source attribution. The current
card has 23 available photos out of 24. Unavailable or failed images display
initials without substituting another person's photograph.
