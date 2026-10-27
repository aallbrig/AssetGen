---
title: "assetgen · Texture Upscaler"
emoji: 🔍
colorFrom: blue
colorTo: indigo
sdk: gradio
sdk_version: "5.23.0"
app_file: app.py
pinned: false
license: apache-2.0
hardware: zero-gpu
tags:
  - super-resolution
  - texture-upscaling
  - game-assets
  - real-esrgan
  - assetgen
short_description: 4× AI texture upscaling using Real-ESRGAN
---

# assetgen · Texture Upscaler

Upscale game textures up to 4× using Real-ESRGAN AI super-resolution.
Input is capped at 512×512 to stay within ZeroGPU time limits.
Part of the [assetgen](https://github.com/aallbrig/assetgen) pipeline.

**CLI equivalent:** `assetgen gen visual texture upscale input.png --scale 4 --wait`
**Model:** [ai-forever/Real-ESRGAN](https://huggingface.co/ai-forever/Real-ESRGAN)
