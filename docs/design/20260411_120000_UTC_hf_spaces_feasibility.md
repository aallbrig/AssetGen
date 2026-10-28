# HuggingFace Spaces — Feasibility Analysis for AssetGen Generation Commands

_Generated: 2026-04-11 12:00:00 UTC_

This document is the reference input for the HF Spaces implementation agents. Read this first,
then proceed to the implementation spec documents.

---

## 1. Namespace Convention

HuggingFace Space repo names use dots as namespace separators, matching the pattern the user
established via examples:

| Rule | Example |
|------|---------|
| Drop the `gen` CLI prefix | `assetgen gen audio sfx generate` → `AssetGen.audio.sfx.generate` |
| Drop the `visual` CLI domain prefix | `assetgen gen visual rig auto` → `AssetGen.rig.auto` |
| Drop the `support` CLI grouping prefix | `assetgen gen support narrative dialogue npc` → `AssetGen.narrative.dialogue.npc` |
| Keep all other domain prefixes (`audio`, `scene`, `procedural`, `pipeline`, `qa`, `narrative`, `data`) | `assetgen gen scene lighting hdri` → `AssetGen.scene.lighting.hdri` |

**Full mapping table is in Section 3.**

The HF repo creation command pattern is:
```bash
hf repo create assetgen.audio.sfx.generate --repo-type space --space-sdk gradio
```
Repos are created under your authenticated HF account. The full URL will be
`https://huggingface.co/spaces/{YOUR_HF_USERNAME}/AssetGen.audio.sfx.generate`.

---

## 1b. Technical Integration Architecture

See `20260411_120400_UTC_hf_spaces_packaging_and_sdk.md` for full details. Summary:

| Decision | Choice | Rationale |
|----------|--------|-----------|
| How Spaces call AssetGen | `AssetGen.sdk.run(job_type, params)` | Stable public API; handlers maintained once |
| Package install in Space | `AssetGen[spaces]` from PyPI | Single `requirements.txt` line per Space |
| audiocraft (not on PyPI) | `audiocraft @ git+...` added by sync script | Unavoidable until Meta publishes to PyPI |
| Space source location | `spaces/AssetGen.<name>/` in this repo | Single source of truth; CI syncs to HF Hub on tag |
| CI trigger | Same semver tag as release.yml | PyPI publish fires first, then Spaces sync |
| CPU vs ZeroGPU | Per-space `hardware:` in README.md | ~30 CPU-only, ~27 ZeroGPU |

**Prerequisite before any Space can go live:** Add PyPI publish step to `release.yml`
(see `20260411_120300_UTC_repo_health_improvements.md` Section 0.1).

---

## 2. HuggingFace Spaces Platform Constraints

Understanding these constraints drives the feasibility decisions below.

| Constraint | Details |
|-----------|---------|
| **Free CPU tier** | 2 vCPUs, 16 GB RAM, no GPU. Python 3.10. Fine for algorithmic / non-ML tasks. |
| **ZeroGPU** | Shared NVIDIA A100 (80 GB VRAM). Jobs queued dynamically. Use `@spaces.GPU` decorator. ~60 s limit per invocation. Free but rate-limited. |
| **Dedicated GPU tiers** | T4 small ($0.60/hr), A10G small ($3.15/hr), A100 ($4.13/hr). Required for models >20 GB or long inference. |
| **No persistent storage** | `/tmp` only. No writes outside the Space repo directory between requests. |
| **No privileged binaries** | Cannot install Blender, game engines, or arbitrary native Linux packages beyond what pip/apt provides. |
| **File upload limits** | Gradio default is 200 MB per upload. Large mesh files (>50 MB) will be close to the edge. |
| **Inference timeout** | ZeroGPU hard-kills after ~60 s per GPU call. Very large models (Hunyuan3D-2) may need dedicated GPU. |
| **`spaces` package** | Pre-installed in HF Spaces environments. Import with `import spaces`; no `requirements.txt` entry needed. |
| **HF Hub model cache** | Models are downloaded to `/tmp` on cold start. Large models add significant cold-start time. |

---

## 3. Complete Feasibility Matrix

### 3a. Visual Domain (drops `visual.` prefix in namespace)

| CLI Command | HF Space Name | Feasible | Tier | Hardware | Primary Model |
|-------------|---------------|----------|------|----------|---------------|
| `assetgen gen visual concept generate` | `AssetGen.concept.generate` | ✅ | 1 | ZeroGPU | SDXL Base 1.0 |
| `assetgen gen visual concept style` | `AssetGen.concept.style` | ✅ | 2 | ZeroGPU | IP-Adapter + SDXL |
| `assetgen gen visual blockout create` | `AssetGen.blockout.create` | ✅ | 3 | ZeroGPU | SDXL (renders sketch) |
| `assetgen gen visual model create` | `AssetGen.model.create` | ✅ | 1 | ZeroGPU (A100) | Hunyuan3D-2 |
| `assetgen gen visual model multiview` | `AssetGen.model.multiview` | ✅ | 2 | ZeroGPU | Zero123++ |
| `assetgen gen visual model splat` | `AssetGen.model.splat` | ✅ | 2 | ZeroGPU | TripoSR |
| `assetgen gen visual model retopo` | `AssetGen.model.retopo` | ❌ | — | — | Blender required |
| `assetgen gen visual mesh validate` | `AssetGen.mesh.validate` | ✅ | 2 | CPU | trimesh |
| `assetgen gen visual mesh convert` | `AssetGen.mesh.convert` | ✅ | 3 | CPU | trimesh |
| `assetgen gen visual mesh merge` | `AssetGen.mesh.merge` | ✅ | 3 | CPU | trimesh |
| `assetgen gen visual mesh bounds` | `AssetGen.mesh.bounds` | ✅ | 3 | CPU | trimesh |
| `assetgen gen visual mesh flipnormals` | `AssetGen.mesh.flipnormals` | ✅ | 3 | CPU | trimesh |
| `assetgen gen visual mesh weld` | `AssetGen.mesh.weld` | ✅ | 3 | CPU | trimesh |
| `assetgen gen visual mesh center` | `AssetGen.mesh.center` | ✅ | 3 | CPU | trimesh |
| `assetgen gen visual mesh scale` | `AssetGen.mesh.scale` | ✅ | 3 | CPU | trimesh |
| `assetgen gen visual lod generate` | `AssetGen.lod.generate` | ✅ | 3 | CPU | pyfqmr |
| `assetgen gen visual uv auto` | `AssetGen.uv.auto` | ✅ | 3 | CPU | xatlas |
| `assetgen gen visual texture generate` | `AssetGen.texture.generate` | ✅ | 1 | ZeroGPU | SDXL Base 1.0 |
| `assetgen gen visual texture from_concept` | `AssetGen.texture.from_concept` | ✅ | 2 | ZeroGPU | IP-Adapter + SDXL |
| `assetgen gen visual texture pbr` | `AssetGen.texture.pbr` | ✅ | 3 | CPU | algorithmic (Pillow) |
| `assetgen gen visual texture bake` | `AssetGen.texture.bake` | ❌ | — | — | Blender renderer required |
| `assetgen gen visual texture inpaint` | `AssetGen.texture.inpaint` | ✅ | 2 | ZeroGPU | SDXL Inpainting |
| `assetgen gen visual texture upscale` | `AssetGen.texture.upscale` | ✅ | 1 | ZeroGPU | Real-ESRGAN x4+ |
| `assetgen gen visual texture channel_pack` | `AssetGen.texture.channel_pack` | ✅ | 3 | CPU | Pillow |
| `assetgen gen visual texture convert` | `AssetGen.texture.convert` | ✅ | 3 | CPU | Pillow |
| `assetgen gen visual texture atlas_pack` | `AssetGen.texture.atlas_pack` | ✅ | 3 | CPU | Pillow |
| `assetgen gen visual texture mipmap` | `AssetGen.texture.mipmap` | ✅ | 3 | CPU | Pillow |
| `assetgen gen visual texture normalmap_convert` | `AssetGen.texture.normalmap_convert` | ✅ | 3 | CPU | Pillow |
| `assetgen gen visual texture seamless` | `AssetGen.texture.seamless` | ✅ | 3 | CPU | Pillow |
| `assetgen gen visual texture resize` | `AssetGen.texture.resize` | ✅ | 3 | CPU | Pillow |
| `assetgen gen visual texture report` | `AssetGen.texture.report` | ✅ | 3 | CPU | Pillow |
| `assetgen gen visual rig auto` | `AssetGen.rig.auto` | ✅ | 2 | ZeroGPU | UniRig |
| `assetgen gen visual animate keyframe` | `AssetGen.animate.keyframe` | ✅ | 2 | ZeroGPU | AnimateDiff v1.5 |
| `assetgen gen visual animate mocap` | `AssetGen.animate.mocap` | ✅ | 2 | ZeroGPU | Sapiens Pose 0.3B |
| `assetgen gen visual animate retarget` | `AssetGen.animate.retarget` | ❌ | — | — | Skeletal solver (Blender/BVH) required |
| `assetgen gen visual vfx particle` | `AssetGen.vfx.particle` | ✅ | 3 | CPU | Pillow + numpy |
| `assetgen gen visual ui icon` | `AssetGen.ui.icon` | ✅ | 2 | ZeroGPU | SDXL |
| `assetgen gen visual ui button` | `AssetGen.ui.button` | ✅ | 3 | ZeroGPU | SDXL |
| `assetgen gen visual ui panel` | `AssetGen.ui.panel` | ✅ | 3 | ZeroGPU | SDXL |
| `assetgen gen visual ui widget` | `AssetGen.ui.widget` | ✅ | 3 | ZeroGPU | SDXL |
| `assetgen gen visual ui mockup` | `AssetGen.ui.mockup` | ✅ | 2 | ZeroGPU | ControlNet + SDXL |
| `assetgen gen visual ui layout` | `AssetGen.ui.layout` | ✅ | 3 | ZeroGPU | SDXL |
| `assetgen gen visual ui iconset` | `AssetGen.ui.iconset` | ✅ | 3 | ZeroGPU | SDXL |
| `assetgen gen visual ui theme` | `AssetGen.ui.theme` | ✅ | 3 | ZeroGPU | SDXL |
| `assetgen gen visual ui screen` | `AssetGen.ui.screen` | ✅ | 3 | ZeroGPU | SDXL |
| `assetgen gen visual sprite pack` | `AssetGen.sprite.pack` | ✅ | 3 | CPU | Pillow |

### 3b. Audio Domain

| CLI Command | HF Space Name | Feasible | Tier | Hardware | Primary Model |
|-------------|---------------|----------|------|----------|---------------|
| `assetgen gen audio sfx generate` | `AssetGen.audio.sfx.generate` | ✅ | 1 | ZeroGPU | AudioGen Medium |
| `assetgen gen audio music compose` | `AssetGen.audio.music.compose` | ✅ | 1 | ZeroGPU | MusicGen Medium |
| `assetgen gen audio music loop` | `AssetGen.audio.music.loop` | ✅ | 2 | ZeroGPU | MusicGen Medium |
| `assetgen gen audio music adaptive` | `AssetGen.audio.music.adaptive` | ✅ | 3 | ZeroGPU | MusicGen Large |
| `assetgen gen audio ambient generate` | `AssetGen.audio.ambient.generate` | ✅ | 2 | ZeroGPU | MusicGen Stereo Large |
| `assetgen gen audio voice tts` | `AssetGen.audio.voice.tts` | ✅ | 1 | ZeroGPU | Bark (suno/bark) |
| `assetgen gen audio voice clone` | `AssetGen.audio.voice.clone` | ✅ | 2 | ZeroGPU | XTTS-v2 |
| `assetgen gen audio process normalize` | `AssetGen.audio.process.normalize` | ✅ | 3 | CPU | pydub + pyloudnorm |
| `assetgen gen audio process trim_silence` | `AssetGen.audio.process.trim_silence` | ✅ | 3 | CPU | pydub |
| `assetgen gen audio process loop_optimize` | `AssetGen.audio.process.loop_optimize` | ✅ | 3 | CPU | scipy |
| `assetgen gen audio process convert` | `AssetGen.audio.process.convert` | ✅ | 3 | CPU | pydub (needs ffmpeg) |
| `assetgen gen audio process downmix` | `AssetGen.audio.process.downmix` | ✅ | 3 | CPU | pydub |
| `assetgen gen audio process resample` | `AssetGen.audio.process.resample` | ✅ | 3 | CPU | scipy |
| `assetgen gen audio process waveform` | `AssetGen.audio.process.waveform` | ✅ | 3 | CPU | matplotlib |

### 3c. Scene Domain

| CLI Command | HF Space Name | Feasible | Tier | Hardware | Primary Model |
|-------------|---------------|----------|------|----------|---------------|
| `assetgen gen scene physics collider` | `AssetGen.scene.physics.collider` | ✅ | 3 | CPU | V-HACD / CoACD |
| `assetgen gen scene lighting hdri` | `AssetGen.scene.lighting.hdri` | ✅ | 2 | ZeroGPU | Intel LDM3D-pano |
| `assetgen gen scene depth estimate` | `AssetGen.scene.depth.estimate` | ✅ | 1 | ZeroGPU | Intel DPT-Large |

### 3d. Procedural Domain

| CLI Command | HF Space Name | Feasible | Tier | Hardware | Primary Model |
|-------------|---------------|----------|------|----------|---------------|
| `assetgen gen procedural terrain heightmap` | `AssetGen.procedural.terrain.heightmap` | ✅ | 1 | CPU | numpy / noise |
| `assetgen gen procedural texture noise` | `AssetGen.procedural.texture.noise` | ✅ | 3 | CPU | numpy |
| `assetgen gen procedural level dungeon` | `AssetGen.procedural.level.dungeon` | ✅ | 2 | CPU | BSP / cellular automata |
| `assetgen gen procedural level voronoi` | `AssetGen.procedural.level.voronoi` | ✅ | 3 | CPU | scipy |
| `assetgen gen procedural foliage scatter` | `AssetGen.procedural.foliage.scatter` | ✅ | 3 | CPU | Poisson disk / numpy |
| `assetgen gen procedural tileset wfc` | `AssetGen.procedural.tileset.wfc` | ✅ | 3 | CPU | Wave Function Collapse |
| `assetgen gen procedural plant lsystem` | `AssetGen.procedural.plant.lsystem` | ✅ | 3 | CPU | L-system |

### 3e. Pipeline Domain — ALL INFEASIBLE

| CLI Command | HF Space Name | Feasible | Reason |
|-------------|---------------|----------|--------|
| `assetgen gen pipeline asset manifest` | `AssetGen.pipeline.asset.manifest` | ❌ | Operates on a local game project directory tree; no meaningful web demo |
| `assetgen gen pipeline asset validate` | `AssetGen.pipeline.asset.validate` | ❌ | Same — whole-project file walker |
| `assetgen gen pipeline asset rename` | `AssetGen.pipeline.asset.rename` | ❌ | Same — batch renames local files |
| `assetgen gen pipeline asset report` | `AssetGen.pipeline.asset.report` | ❌ | Same — reads local project tree |
| `assetgen gen pipeline git lfs_rules` | `AssetGen.pipeline.git.lfs_rules` | ❌ | Outputs `.gitattributes` content for a local Git repo; no web demo value |
| `assetgen gen pipeline integrate export` | `AssetGen.pipeline.integrate.export` | ❌ | Requires Unity/Godot/Unreal engine installed locally |

### 3f. Support / Narrative Domain

| CLI Command | HF Space Name | Feasible | Tier | Hardware | Primary Model |
|-------------|---------------|----------|------|----------|---------------|
| `assetgen gen support narrative dialogue npc` | `AssetGen.narrative.dialogue.npc` | ✅ | 1 | ZeroGPU | Phi-3.5-mini-instruct |
| `assetgen gen support narrative dialogue validate` | `AssetGen.narrative.dialogue.validate` | ⚠️ | 3 | CPU | networkx — low demo value |
| `assetgen gen support narrative lore generate` | `AssetGen.narrative.lore.generate` | ✅ | 2 | ZeroGPU | Phi-3.5-mini-instruct |
| `assetgen gen support narrative quest design` | `AssetGen.narrative.quest.design` | ✅ | 2 | ZeroGPU | Phi-3.5-mini-instruct |
| `assetgen gen support narrative quest validate` | `AssetGen.narrative.quest.validate` | ⚠️ | 3 | CPU | networkx — low demo value |
| `assetgen gen support data i18n extract` | `AssetGen.data.i18n.extract` | ❌ | — | — | Extracts strings from local source files; no web demo |

### 3g. QA Domain — ALL INFEASIBLE

| CLI Command | Feasible | Reason |
|-------------|----------|--------|
| `assetgen gen qa validate` | ❌ | Validates a full local game asset project; requires directory context |
| `assetgen gen qa report` | ❌ | Same — whole-project analysis tool |

---

## 4. Infeasibility Justifications (Detail)

### `AssetGen.model.retopo` — Requires Blender
Auto-retopology as implemented depends on Blender's Python API (`bpy`) or a native retopology
solver (e.g., QuadriFlow, Instant Meshes) that compiles from C++ and cannot be pip-installed in
a standard HF Spaces environment. The `pyfqmr` fallback in the AssetGen handler does decimation,
not retopology — the mesh stays triangulated with no quads.

**Potential workaround (not in scope):** A dedicated Blender Docker image on a dedicated GPU
Space could work, but that's a custom Space type, not standard Gradio.

### `AssetGen.texture.bake` — Requires Blender's GPU rasterizer
High-to-low-poly baking requires a rasterization pass: render the high-poly mesh onto the UV
space of the low-poly mesh. This needs either Blender Cycles/EEVEE or a GPU-accelerated OpenGL
rasterizer. Neither is available in HF Spaces' standard pip environment.

### `AssetGen.animate.retarget` — Requires skeletal solver
Retargeting an animation from one skeleton to another requires BVH parsing, bone chain
matching, and inverse kinematics solving. The AssetGen handler uses CMU Mocap data + Blender's
NLA (non-linear animation) system. No pip-installable pure-Python skeletal solver exists that
handles arbitrary rig topologies.

### Pipeline commands — No web demo meaning
These six commands operate on a developer's local game project directory:
- They walk directory trees to find assets
- They write `.gitattributes` or manifest JSON files into the project
- They invoke game engine CLI tools (`unity`, `godot`, `unreal`)

None of these have a useful input/output pair for a Gradio web demo.

### `AssetGen.data.i18n.extract` — Local project operation
Parses source code files (`.cs`, `.gd`, `.lua`, `.py`) within a game project to extract
localization strings. Requires access to a real game project on disk.

### QA commands — Whole-project context required
Both `assetgen gen qa validate` and `assetgen gen qa report` analyze an entire asset project tree:
they check polygon budgets across all meshes, texture resolution consistency, UV island
overlap across the whole atlas. Uploading an entire game project to a web demo is impractical.

---

## 5. Priority Tier Summary

### Tier 1 — Implement First (10 Spaces)
Highest demo value, clearest input/output, best showcase for AssetGen capabilities.
Full implementation specs (complete `app.py`, `requirements.txt`, `README.md`) are in
`20260411_120100_UTC_hf_spaces_spec_tier1.md`.

| # | Space Name | What It Shows |
|---|-----------|----------------|
| 1 | `AssetGen.audio.sfx.generate` | AudioGen: text → game sound effect WAV |
| 2 | `AssetGen.audio.music.compose` | MusicGen: text → game music track |
| 3 | `AssetGen.audio.voice.tts` | Bark: text → expressive NPC speech |
| 4 | `AssetGen.concept.generate` | SDXL: text → game concept art |
| 5 | `AssetGen.texture.generate` | SDXL: text → tileable game texture |
| 6 | `AssetGen.texture.upscale` | Real-ESRGAN: 4× AI texture upscaling |
| 7 | `AssetGen.model.create` | Hunyuan3D-2: image → 3D game asset (.glb) |
| 8 | `AssetGen.scene.depth.estimate` | DPT-Large: image → depth map |
| 9 | `AssetGen.narrative.dialogue.npc` | Phi-3.5: text prompt → NPC dialogue lines |
| 10 | `AssetGen.procedural.terrain.heightmap` | Pure Python: params → terrain heightmap PNG |

### Tier 2 — High Value, Implement After Tier 1 (17 Spaces)
Strong demos but heavier setup or narrower audience. Abbreviated specs in
`20260411_120200_UTC_hf_spaces_spec_tier2_tier3.md`.

`AssetGen.audio.ambient.generate`, `AssetGen.audio.voice.clone`, `AssetGen.audio.music.loop`,
`AssetGen.model.multiview`, `AssetGen.model.splat`, `AssetGen.rig.auto`, `AssetGen.animate.keyframe`,
`AssetGen.animate.mocap`, `AssetGen.concept.style`, `AssetGen.texture.inpaint`,
`AssetGen.texture.from_concept`, `AssetGen.scene.lighting.hdri`, `AssetGen.narrative.lore.generate`,
`AssetGen.narrative.quest.design`, `AssetGen.ui.icon`, `AssetGen.ui.mockup`,
`AssetGen.procedural.level.dungeon`

### Tier 3 — Utility Tools (30+ Spaces)
CPU-only or narrow-use tools. Good for completeness but lower demo impact.
Also listed in `20260411_120200_UTC_hf_spaces_spec_tier2_tier3.md`.

All mesh utilities, audio processing tools, texture utilities, remaining procedural generators,
and `AssetGen.mesh.validate`.

---

## 6. Spaces Summary Counts

| Status | Count |
|--------|-------|
| ✅ Feasible (Tier 1) | 10 |
| ✅ Feasible (Tier 2) | 17 |
| ✅ Feasible (Tier 3) | ~30 |
| ⚠️ Low demo value (technically feasible) | 2 |
| ❌ Infeasible | 12 |
| **Total commands analyzed** | **82** |
