---
title: "assetgen · Terrain Heightmap Generator"
emoji: 🏔️
colorFrom: green
colorTo: yellow
sdk: gradio
sdk_version: "5.23.0"
app_file: app.py
pinned: false
license: apache-2.0
hardware: cpu-basic
tags:
  - procedural-generation
  - terrain
  - heightmap
  - game-assets
  - assetgen
short_description: Generate procedural terrain heightmaps — CPU only, instant
---

# assetgen · Terrain Heightmap Generator

Generate procedural terrain heightmaps using fractal Perlin noise.
CPU only — no GPU wait, results are instant.
Part of the [assetgen](https://github.com/aallbrig/assetgen) pipeline.

**CLI equivalent:** `assetgen gen procedural terrain heightmap --width 512 --height 512 --seed 42`
