---
title: "assetgen · Texture from Concept Art"
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
  - texture-generation
  - style-transfer
  - game-assets
  - ip-adapter
  - sdxl
  - assetgen
short_description: Tileable textures guided by concept art (IP-Adapter)
---

# assetgen · Texture from Concept Art

Generate tileable PBR-ready textures guided by a concept art style reference.
Uses IP-Adapter + SDXL with automatic seamless texture prompt engineering.
Part of the [assetgen](https://github.com/aallbrig/assetgen) pipeline.

**CLI equivalent:** `assetgen gen visual texture from-concept concept.png "stone wall" --wait`
**Model:** [h94/IP-Adapter](https://huggingface.co/h94/IP-Adapter) + SDXL
