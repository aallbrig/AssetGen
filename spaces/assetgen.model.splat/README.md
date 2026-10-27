---
title: "assetgen · Image-to-3D (TripoSR)"
emoji: 🗿
colorFrom: gray
colorTo: blue
sdk: gradio
sdk_version: "5.23.0"
app_file: app.py
pinned: false
license: apache-2.0
hardware: zero-gpu
tags:
  - 3d-generation
  - image-to-3d
  - game-assets
  - triposr
  - assetgen
short_description: Image-to-3D mesh reconstruction using TripoSR
---

# assetgen · Image-to-3D (TripoSR)

Convert a single foreground image to a 3D GLB mesh using TripoSR.
Part of the [assetgen](https://github.com/aallbrig/assetgen) pipeline.

**CLI equivalent:** `assetgen gen visual model splat input.png --wait`
**Model:** [stabilityai/TripoSR](https://huggingface.co/stabilityai/TripoSR)
