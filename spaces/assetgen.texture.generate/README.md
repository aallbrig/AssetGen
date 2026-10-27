---
title: "assetgen · Texture Generator"
emoji: 🧱
colorFrom: yellow
colorTo: red
sdk: gradio
sdk_version: "5.23.0"
app_file: app.py
pinned: false
license: apache-2.0
hardware: zero-gpu
tags:
  - image-generation
  - texture-generation
  - game-assets
  - stable-diffusion
  - assetgen
short_description: Generate tileable game textures from text using SDXL
---

# assetgen · Texture Generator

Generate seamless tileable PBR-ready albedo textures from text descriptions.
The handler automatically applies texture-specific prompt guidance (seamless, top-down, uniform lighting).
Part of the [assetgen](https://github.com/aallbrig/assetgen) pipeline.

**CLI equivalent:** `assetgen gen visual texture generate "rough stone wall" --wait`
**Model:** [stabilityai/stable-diffusion-xl-base-1.0](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0)
