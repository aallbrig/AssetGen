---
title: "assetgen · NPC Dialogue Generator"
emoji: 💬
colorFrom: pink
colorTo: purple
sdk: gradio
sdk_version: "5.23.0"
app_file: app.py
pinned: false
license: apache-2.0
hardware: zero-gpu
tags:
  - text-generation
  - npc-dialogue
  - game-writing
  - phi
  - assetgen
short_description: NPC dialogue generation using Phi-3.5
---

# assetgen · NPC Dialogue Generator

Generate game NPC dialogue from character descriptions and player queries using Phi-3.5-mini.
Part of the [assetgen](https://github.com/aallbrig/assetgen) pipeline.

**CLI equivalent:** `assetgen gen support narrative dialogue npc --persona "..." --player "..." --wait`
**Model:** [microsoft/Phi-3.5-mini-instruct](https://huggingface.co/microsoft/Phi-3.5-mini-instruct)
