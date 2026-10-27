---
title: "assetgen · Depth Estimator"
emoji: 📐
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: "5.23.0"
app_file: app.py
pinned: false
license: apache-2.0
hardware: zero-gpu
tags:
  - depth-estimation
  - computer-vision
  - game-assets
  - dpt
  - assetgen
short_description: Monocular depth estimation for game scenes using DPT-Large
---

# assetgen · Depth Estimator

Generate depth maps from game scene images using Intel DPT-Large.
Useful for depth-of-field setup, scene geometry estimation, and depth compositing.
Part of the [assetgen](https://github.com/aallbrig/assetgen) pipeline.

**CLI equivalent:** `assetgen gen scene depth estimate scene.png --wait`
**Model:** [Intel/dpt-large](https://huggingface.co/Intel/dpt-large)
