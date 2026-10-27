---
title: "assetgen · NPC Voice TTS"
emoji: 🎙️
colorFrom: green
colorTo: green
sdk: gradio
sdk_version: "5.23.0"
app_file: app.py
pinned: false
license: apache-2.0
hardware: zero-gpu
tags:
  - audio
  - text-to-speech
  - game-assets
  - bark
  - assetgen
short_description: Generate expressive NPC voices from text using Bark
---

# assetgen · NPC Voice TTS

Generate expressive NPC speech — including `[laughs]`, `[sighs]`, `[gasps]` — using Bark.
Part of the [assetgen](https://github.com/aallbrig/assetgen) pipeline.

**CLI equivalent:** `assetgen gen audio voice tts "Halt! Who goes there?" --voice v2/en_speaker_6`
**Model:** [suno/bark](https://huggingface.co/suno/bark)
