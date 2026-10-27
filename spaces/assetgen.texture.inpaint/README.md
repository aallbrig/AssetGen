---
title: "assetgen · Texture Inpainting"
emoji: 🖼️
colorFrom: yellow
colorTo: red
sdk: gradio
sdk_version: "5.23.0"
app_file: app.py
pinned: false
license: apache-2.0
hardware: zero-gpu
tags:
  - inpainting
  - texture-generation
  - game-assets
  - sdxl
  - assetgen
short_description: Fill masked texture regions with SDXL Inpainting
---

# assetgen · Texture Inpainting

Fill masked regions of a game texture using SDXL Inpainting.
Upload a texture and a white-on-black mask, describe what to fill in.
Part of the [assetgen](https://github.com/aallbrig/assetgen) pipeline.

**CLI equivalent:** `assetgen gen visual texture inpaint texture.png --mask mask.png --wait`
**Model:** [diffusers/stable-diffusion-xl-1.0-inpainting-0.1](https://huggingface.co/diffusers/stable-diffusion-xl-1.0-inpainting-0.1)
