# HuggingFace Spaces — Tier 2 & Tier 3 Implementation Spec

_Generated: 2026-04-11 12:02:00 UTC_
_Prerequisite: read `20260411_120000_UTC_hf_spaces_feasibility.md` and complete Tier 1 first._

This document provides **abbreviated specs** for Tier 2 and Tier 3 Spaces. Each entry gives:
- Creation command
- Hardware tier
- Primary model + pip package
- Input/output description for the Gradio UI
- Key implementation notes
- `requirements.txt` content (**reference only** — see note below)

The implementing agent should follow the exact same file structure and patterns from the Tier 1
spec (`20260411_120100_UTC_hf_spaces_spec_tier1.md`) — only the inference logic and UI differ.

**Required for every new Space (including all Tier 2/3):** Follow the "New Space Checklist" in
the Tier 1 spec. This includes adding a PyCharm run config by updating `SPACES` in
`scripts/generate_run_configs.py` and running the script. Do not create a space without its
corresponding `.idea/runConfigurations/space_AssetGen_<name>.xml`.

> **`requirements.txt` blocks are for reference only — do NOT create them in the repo.**
> Per the packaging decision in `20260411_120400_UTC_hf_spaces_packaging_and_sdk.md` Section 4,
> each Space directory contains only `app.py` and `README.md`. The `requirements.txt` is
> **generated dynamically** by `scripts/sync_spaces.py` at upload time and is never stored
> in the repository. The blocks below document which packages each Space needs; that information
> is already encoded in the `AUDIOCRAFT_SPACES` and `CPU_SPACES` sets in `sync_spaces.py`.

---

## Tier 2 Spaces (17 Spaces)

### T2-1: `AssetGen.audio.ambient.generate`

```
hf repo create assetgen.audio.ambient.generate --repo-type space --space-sdk gradio
Hardware: zero-gpu
Model: facebook/musicgen-stereo-large
Package: audiocraft (same git install as Tier 1 audio spaces)
```

**UI Inputs:** `Textbox` (ambient description), `Slider` (duration 10–60 s, default 20)
**UI Output:** `Audio` (stereo WAV)
**Notes:**
- Use `MusicGen.get_pretrained("facebook/musicgen-stereo-large")` — this is the stereo variant
- `musicgen-stereo-large` is ~3.3 GB. ZeroGPU should handle it.
- Prompt examples: "eerie cave drips echoing", "bustling market square ambience", "thunderstorm at sea"

**requirements.txt:**
```
audiocraft @ git+https://github.com/facebookresearch/audiocraft.git
torch>=2.3.0
torchaudio>=2.3.0
gradio>=4.44.0
```

---

### T2-2: `AssetGen.audio.voice.clone`

```
hf repo create assetgen.audio.voice.clone --repo-type space --space-sdk gradio
Hardware: zero-gpu
Model: coqui-ai/XTTS-v2
Package: coqui-tts (TTS on PyPI)
```

**UI Inputs:**
- `Audio` upload (reference voice clip, 5–30 s WAV/MP3)
- `Textbox` (text to synthesize in the cloned voice)
- `Dropdown` (language: en, es, fr, de, it, pt, nl, pl, cs, ar, tr, ru, hi, zh)

**UI Output:** `Audio` (synthesized WAV in cloned voice)

**Notes:**
- `pip install TTS` installs the Coqui TTS package. The class is `TTS` from `TTS.api`.
- Usage pattern:
  ```python
  from TTS.api import TTS
  tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
  tts.tts_to_file(
      text=text,
      speaker_wav=reference_audio_path,
      language=language,
      file_path=output_path,
  )
  ```
- The reference audio should be saved to a temp file (Gradio provides path).
- Cold start is slow (~60 s). Note this in the Space description.
- Gradio's `Audio` input with `type="filepath"` is best here.

**requirements.txt:**
```
TTS>=0.22.0
torch>=2.3.0
gradio>=4.44.0
```

---

### T2-3: `AssetGen.audio.music.loop`

```
hf repo create assetgen.audio.music.loop --repo-type space --space-sdk gradio
Hardware: zero-gpu
Model: facebook/musicgen-medium
Package: audiocraft (same as other audio spaces)
```

**UI Inputs:**
- `Textbox` (music description)
- `Slider` (segment duration 5–15 s)
- `Slider` (number of loops to generate: 1–4)

**UI Output:** `Audio` (looped WAV)

**Notes:**
- Generate N short clips and concatenate them with `torchaudio.save`.
- For true seamless loops, crossfade the last 0.5 s of each clip with the first 0.5 s of the next.
- Simple crossfade formula: `output[i] = clip_a[i] * fade_out[i] + clip_b[i] * fade_in[i]`
- The `fade_out` and `fade_in` are linear ramps over the crossfade region.

**requirements.txt:**
```
audiocraft @ git+https://github.com/facebookresearch/audiocraft.git
torch>=2.3.0
torchaudio>=2.3.0
gradio>=4.44.0
numpy>=1.26.0
```

---

### T2-4: `AssetGen.model.multiview`

```
hf repo create assetgen.model.multiview --repo-type space --space-sdk gradio
Hardware: zero-gpu
Model: sudo-ai/zero123plus
Package: diffusers>=0.28.0
```

**UI Inputs:** `Image` upload (single view of an object, ideally white background)
**UI Output:** `Gallery` (6 surrounding views: front, front-left, left, back-left, back, back-right)

**Notes:**
- Zero123++ is in `diffusers`. Load with:
  ```python
  from diffusers import StableDiffusionPipeline
  # Zero123++ uses a custom pipeline — load from model card instructions
  pipeline = DiffusionPipeline.from_pretrained(
      "sudo-ai/zero123plus",
      custom_pipeline="sudo-ai/zero123plus",
      torch_dtype=torch.float16,
  )
  ```
- The output is a 3×2 grid of 6 views. Split it into 6 images for the Gallery.
- Input image should be square; resize to 256×256 before inference.
- Gallery should show all 6 views simultaneously.

**requirements.txt:**
```
diffusers>=0.28.0
transformers>=4.40.0
accelerate>=0.30.0
torch>=2.3.0
Pillow>=10.0.0
gradio>=4.44.0
```

---

### T2-5: `AssetGen.model.splat`

```
hf repo create assetgen.model.splat --repo-type space --space-sdk gradio
Hardware: zero-gpu
Model: stabilityai/TripoSR
Package: tsr (TripoSR package from GitHub)
```

**UI Inputs:**
- `Image` upload (single foreground image)
- `Checkbox` (remove background before processing, default True)

**UI Output:** `Model3D` (GLB mesh)

**Notes:**
- TripoSR has an official HF Space at `stabilityai/TripoSR` with source code to reference.
- Install: `pip install git+https://github.com/VAST-AI-Research/TripoSR.git`
- Usage:
  ```python
  from tsr.system import TSR
  model = TSR.from_pretrained("stabilityai/TripoSR")
  model.to("cuda")
  scene_codes = model(image, device="cuda")
  mesh = model.extract_mesh(scene_codes)[0]
  mesh.export(output_path)
  ```
- Background removal: use `rembg` (`pip install rembg`).
- Input image should be resized to 512×512.

**requirements.txt:**
```
tsr @ git+https://github.com/VAST-AI-Research/TripoSR.git
rembg>=2.0.57
torch>=2.3.0
torchvision>=0.18.0
trimesh>=3.21.0
Pillow>=10.0.0
gradio>=4.44.0
```

---

### T2-6: `AssetGen.rig.auto`

```
hf repo create assetgen.rig.auto --repo-type space --space-sdk gradio
Hardware: zero-gpu
Model: VAST-AI/UniRig
Package: unicore / unirig (custom, check model card)
```

**UI Inputs:** `File` upload (GLB or OBJ mesh)
**UI Output:** `File` download (rigged GLB) + `Model3D` preview

**Notes:**
- UniRig (`VAST-AI/UniRig`) is a research model. Check the model card at
  `https://huggingface.co/VAST-AI/UniRig` for the official installation and inference API.
  The implementation details may differ from what AssetGen's handler assumes.
- If UniRig requires a custom conda environment or compiled extensions that pip cannot install,
  this Space may need to be demoted to "infeasible until packaging improves."
- Fallback: show a note in the UI saying "UniRig requires additional setup — use AssetGen CLI."
- The `gr.Model3D` component can display the rigged GLB (bones are not visible in the viewer,
  but the skinned mesh will load correctly).

**requirements.txt:**
```
# Check VAST-AI/UniRig model card for exact install command
# Likely: unirig @ git+https://github.com/VAST-AI-Research/UniRig.git
torch>=2.3.0
trimesh>=3.21.0
gradio>=4.44.0
```

---

### T2-7: `AssetGen.animate.keyframe`

```
hf repo create assetgen.animate.keyframe --repo-type space --space-sdk gradio
Hardware: zero-gpu
Model: guoyww/animatediff-motion-adapter-v1-5-2 + stabilityai/stable-diffusion-v1-5
Package: diffusers>=0.28.0
```

**UI Inputs:**
- `Textbox` (motion/animation description, e.g. "a warrior swinging a sword")
- `Slider` (number of frames: 8–16, default 16)
- `Slider` (guidance scale: 7–12)
- `Number` (seed)

**UI Output:** `Video` (MP4 / GIF of the animation frames)

**Notes:**
- AnimateDiff combines a motion adapter with a base SD1.5 checkpoint.
- Load with:
  ```python
  from diffusers import AnimateDiffPipeline, MotionAdapter, DDIMScheduler
  adapter = MotionAdapter.from_pretrained("guoyww/animatediff-motion-adapter-v1-5-2")
  pipe = AnimateDiffPipeline.from_pretrained(
      "emilianJR/epiCRealism",  # or any SD1.5 fine-tune
      motion_adapter=adapter,
      torch_dtype=torch.float16,
  )
  pipe.scheduler = DDIMScheduler.from_config(pipe.scheduler.config, beta_schedule="linear")
  frames = pipe(prompt=prompt, num_frames=16).frames[0]
  ```
- Export frames to GIF using Pillow or MP4 using `imageio`.
- ZeroGPU should handle this; model is ~3 GB total.

**requirements.txt:**
```
diffusers>=0.28.0
transformers>=4.40.0
accelerate>=0.30.0
torch>=2.3.0
Pillow>=10.0.0
imageio>=2.34.0
imageio-ffmpeg>=0.4.9
gradio>=4.44.0
```

---

### T2-8: `AssetGen.animate.mocap`

```
hf repo create assetgen.animate.mocap --repo-type space --space-sdk gradio
Hardware: zero-gpu
Model: facebook/sapiens-pose-0.3b
Package: transformers>=4.40.0
```

**UI Inputs:** `Image` upload (single image of a person/character) or `Video` (short clip)
**UI Output:** `Image` (pose keypoints overlay) + `JSON` (raw keypoint coordinates)

**Notes:**
- Sapiens Pose is a human pose estimation model.
- Load via `transformers` pipeline:
  ```python
  from transformers import pipeline
  pose_estimator = pipeline(
      "image-segmentation",  # or the specific task type — check model card
      model="facebook/sapiens-pose-0.3b",
      device="cuda",
  )
  ```
  Check the exact task type on the model card; it may be `pose-estimation` or a custom task.
- Keypoints should be drawn on the original image using Pillow (circles + lines).
- For video input, process each frame and output an annotated video.

**requirements.txt:**
```
transformers>=4.40.0
torch>=2.3.0
Pillow>=10.0.0
numpy>=1.26.0
gradio>=4.44.0
```

---

### T2-9: `AssetGen.concept.style`

```
hf repo create assetgen.concept.style --repo-type space --space-sdk gradio
Hardware: zero-gpu
Model: h94/IP-Adapter + stabilityai/stable-diffusion-xl-base-1.0
Package: diffusers>=0.28.0
```

**UI Inputs:**
- `Image` upload (style reference image)
- `Textbox` (content prompt: what to generate)
- `Slider` (style strength: 0.0–1.0, default 0.6)
- `Slider` (steps: 20–40, default 30)

**UI Output:** `Image` (generated image with the reference style applied)

**Notes:**
- IP-Adapter for SDXL is in `diffusers` as `IPAdapterMixin`.
- Load pattern:
  ```python
  from diffusers import StableDiffusionXLPipeline
  pipe = StableDiffusionXLPipeline.from_pretrained("stabilityai/stable-diffusion-xl-base-1.0", torch_dtype=torch.float16)
  pipe.load_ip_adapter("h94/IP-Adapter", subfolder="sdxl_models", weight_name="ip-adapter_sdxl.bin")
  pipe.set_ip_adapter_scale(style_strength)
  images = pipe(prompt=prompt, ip_adapter_image=style_image).images
  ```
- The `style_strength` slider controls `set_ip_adapter_scale()`.

**requirements.txt:**
```
diffusers>=0.28.0
transformers>=4.40.0
accelerate>=0.30.0
torch>=2.3.0
Pillow>=10.0.0
gradio>=4.44.0
```

---

### T2-10: `AssetGen.texture.inpaint`

```
hf repo create assetgen.texture.inpaint --repo-type space --space-sdk gradio
Hardware: zero-gpu
Model: diffusers/stable-diffusion-xl-1.0-inpainting-0.1
Package: diffusers>=0.28.0
```

**UI Inputs:**
- `Image` (original texture — use Gradio's `Image` with `tool="sketch"` for mask drawing)
- `Textbox` (prompt: what to fill the masked area with)
- `Slider` (steps: 20–40)

**UI Output:** `Image` (inpainted texture)

**Notes:**
- Gradio's `gr.Image(tool="sketch", source="upload")` enables drawing a mask directly.
- Or provide separate `Image` upload (texture) + `Image` upload (mask as B&W image).
- The mask in SDXL inpainting is white-on-black (white = inpaint here).
- Load:
  ```python
  from diffusers import StableDiffusionXLInpaintPipeline
  pipe = StableDiffusionXLInpaintPipeline.from_pretrained(
      "diffusers/stable-diffusion-xl-1.0-inpainting-0.1",
      torch_dtype=torch.float16,
  )
  result = pipe(prompt=prompt, image=image, mask_image=mask, strength=0.99).images[0]
  ```

**requirements.txt:**
```
diffusers>=0.28.0
transformers>=4.40.0
accelerate>=0.30.0
torch>=2.3.0
Pillow>=10.0.0
gradio>=4.44.0
```

---

### T2-11: `AssetGen.texture.from_concept`

```
hf repo create assetgen.texture.from_concept --repo-type space --space-sdk gradio
Hardware: zero-gpu
Model: h94/IP-Adapter + stabilityai/stable-diffusion-xl-base-1.0
Package: diffusers>=0.28.0
```

Same implementation as `AssetGen.concept.style` but with the texture suffix prompt engineering
from `AssetGen.texture.generate` applied automatically.

**UI Inputs:** `Image` (concept art reference), `Textbox` (surface/material description), `Slider` (style strength)
**UI Output:** `Image` (tileable texture guided by the concept art style)

---

### T2-12: `AssetGen.scene.lighting.hdri`

```
hf repo create assetgen.scene.lighting.hdri --repo-type space --space-sdk gradio
Hardware: zero-gpu
Model: Intel/ldm3d-pano
Package: diffusers>=0.28.0
```

**UI Inputs:** `Textbox` (scene/sky description: "sunset over desert dunes")
**UI Output:** `Image` (equirectangular panorama, 2:1 aspect ratio)

**Notes:**
- LDM3D-pano generates a 360° panorama from text.
- Load with diffusers:
  ```python
  from diffusers import StableDiffusionLDM3DPipeline
  pipe = StableDiffusionLDM3DPipeline.from_pretrained("Intel/ldm3d-pano")
  output = pipe(prompt=prompt, width=1024, height=512)
  rgb_image = output.rgb[0]
  ```
- The output should be downloadable as EXR or high-quality PNG for use as HDRI in game engines.
  Note: the LDM3D model outputs an RGB image + depth map. The RGB is the panorama.
- For true HDRI (HDR values), a dedicated HDR pipeline or post-processing is needed.
  Label the output clearly as "HDR panorama reference (LDR PNG)" in the UI.

**requirements.txt:**
```
diffusers>=0.28.0
transformers>=4.40.0
accelerate>=0.30.0
torch>=2.3.0
Pillow>=10.0.0
gradio>=4.44.0
```

---

### T2-13: `AssetGen.narrative.lore.generate`

```
hf repo create assetgen.narrative.lore.generate --repo-type space --space-sdk gradio
Hardware: zero-gpu
Model: microsoft/Phi-3.5-mini-instruct
```

**UI Inputs:**
- `Textbox` (world/setting description: "a steampunk empire in perpetual smog")
- `Dropdown` (lore type: History, Faction, Location, Artifact, Myth/Legend, Religion)
- `Slider` (word count: 100–400)

**UI Output:** `Textbox` (generated lore text)

**Notes:** Same model load pattern as `AssetGen.narrative.dialogue.npc`. System prompt:
> "You are a world-building writer creating rich game lore entries. Write immersive,
> detailed lore that feels authentic to the setting. Use in-world terminology and avoid
> generic fantasy/sci-fi tropes."

---

### T2-14: `AssetGen.narrative.quest.design`

```
hf repo create assetgen.narrative.quest.design --repo-type space --space-sdk gradio
Hardware: zero-gpu
Model: microsoft/Phi-3.5-mini-instruct
```

**UI Inputs:**
- `Textbox` (game world context)
- `Dropdown` (quest type: Main Story, Side Quest, Bounty, Fetch, Escort, Investigation, Boss Hunt)
- `Slider` (number of objectives: 2–6)

**UI Output:** `Textbox` (quest title + objectives + optional twist)

---

### T2-15: `AssetGen.ui.icon`

```
hf repo create assetgen.ui.icon --repo-type space --space-sdk gradio
Hardware: zero-gpu
Model: stabilityai/stable-diffusion-xl-base-1.0
```

**UI Inputs:**
- `Textbox` (icon description: "health potion, red bottle with cork")
- `Dropdown` (icon style: Fantasy RPG, Sci-Fi, Minimalist Flat, Pixel Art, Material Design)
- `Dropdown` (background: Transparent, Black, White, Gradient)

**UI Output:** `Image` (512×512 icon PNG)

**Notes:**
- Prompt engineering prefix: `"game UI icon, {style}, isolated object, {bg_desc}, 512x512, high detail"`
- For transparent background: generate on white, then use PIL to remove white bg via alpha threshold.
  Or append "transparent background, no background" to prompt (less reliable than post-processing).
- A grid of 4 variations is more useful than 1: use `num_images_per_prompt=4` and display as `Gallery`.

---

### T2-16: `AssetGen.ui.mockup`

```
hf repo create assetgen.ui.mockup --repo-type space --space-sdk gradio
Hardware: zero-gpu
Model: diffusers/controlnet-canny-sdxl-1.0 + stabilityai/stable-diffusion-xl-base-1.0
Package: diffusers>=0.28.0, controlnet_aux>=0.0.7
```

**UI Inputs:**
- `Image` upload (wireframe sketch or rough layout drawing)
- `Textbox` (UI description: "fantasy RPG inventory screen, dark theme, gold accents")
- `Slider` (ControlNet conditioning strength: 0.5–1.0)

**UI Output:** `Image` (polished game UI mockup)

**Notes:**
- Extract Canny edges from the wireframe, then use ControlNet-Canny-SDXL to generate.
  ```python
  from controlnet_aux import CannyDetector
  from diffusers import ControlNetModel, StableDiffusionXLControlNetPipeline
  controlnet = ControlNetModel.from_pretrained("diffusers/controlnet-canny-sdxl-1.0", torch_dtype=torch.float16)
  pipe = StableDiffusionXLControlNetPipeline.from_pretrained("stabilityai/stable-diffusion-xl-base-1.0", controlnet=controlnet, torch_dtype=torch.float16)
  canny = CannyDetector()(wireframe_image)
  result = pipe(prompt=prompt, image=canny, controlnet_conditioning_scale=strength).images[0]
  ```

**requirements.txt:**
```
diffusers>=0.28.0
transformers>=4.40.0
accelerate>=0.30.0
controlnet-aux>=0.0.7
torch>=2.3.0
Pillow>=10.0.0
gradio>=4.44.0
```

---

### T2-17: `AssetGen.procedural.level.dungeon`

```
hf repo create assetgen.procedural.level.dungeon --repo-type space --space-sdk gradio
Hardware: cpu-basic
Model: None (pure algorithmic)
```

**UI Inputs:**
- `Slider` (map width: 20–100 tiles)
- `Slider` (map height: 20–100 tiles)
- `Dropdown` (algorithm: BSP (Binary Space Partition), Cellular Automata, Rooms+Corridors)
- `Dropdown` (tile style: ASCII, Color Grid, Dark Fantasy)
- `Number` (seed)

**UI Output:** `Image` (rendered dungeon map PNG) + optional `File` (JSON tilemap for download)

**Notes:**
- BSP: recursively split the map rectangle, then carve rooms in the leaves, connect with corridors.
- Cellular Automata: fill with random noise, then run life-like rules (born if ≥5 neighbors, die if <4).
- Rooms+Corridors: place N random non-overlapping rooms, connect with L-shaped corridors.
- Render to image: use Pillow with tile colors (floor=light grey, wall=dark grey, door=brown).
- JSON tilemap: `{"width": W, "height": H, "tiles": [[0,1,0,...], ...]}` (0=wall, 1=floor, 2=door)

**requirements.txt:**
```
numpy>=1.26.0
Pillow>=10.0.0
gradio>=4.44.0
```

---

## Tier 3 Spaces (CPU Tools — Brief Specs)

All Tier 3 Spaces use `hardware: cpu-basic` in their README frontmatter (no GPU needed).
All follow the same Gradio pattern: upload file(s) → process → download file(s).

For each Space below, the implementing agent should:
1. Run `hf repo create <name> --repo-type space --space-sdk gradio`
2. Create a simple `app.py` using the specified Python packages
3. Set `hardware: cpu-basic` in README frontmatter

---

### Mesh Utilities (7 Spaces)

| Space Name | CLI Command | Input | Output | Key Package | Notes |
|-----------|-------------|-------|--------|-------------|-------|
| `AssetGen.mesh.validate` | `visual mesh validate` | GLB/OBJ upload | Text report (watertight, normals, manifold, bounds) | `trimesh` | Use `trimesh.load()` + `mesh.is_watertight`, `mesh.is_volume`, `mesh.bounds` |
| `AssetGen.mesh.convert` | `visual mesh convert` | GLB/OBJ/PLY/STL upload + format dropdown | Converted file download | `trimesh` | `trimesh.load()` then `mesh.export(output_path)` |
| `AssetGen.mesh.bounds` | `visual mesh bounds` | Mesh upload | AABB min/max, OBB, bounding sphere (text + visual) | `trimesh` | Display as JSON; optionally render bounds wireframe |
| `AssetGen.mesh.center` | `visual mesh center` | Mesh upload | Re-centered mesh download | `trimesh` | `mesh.apply_translation(-mesh.centroid)` |
| `AssetGen.mesh.scale` | `visual mesh scale` | Mesh upload + scale factor slider | Scaled mesh download | `trimesh` | `mesh.apply_scale(factor)` |
| `AssetGen.mesh.flipnormals` | `visual mesh flipnormals` | Mesh upload | Mesh with flipped normals download | `trimesh` | `mesh.invert()` |
| `AssetGen.mesh.weld` | `visual mesh weld` | Mesh upload + tolerance slider | Welded mesh download + vert count delta | `trimesh` | `trimesh.smoothing.filter_mut_diffs(mesh, ...)` or `trimesh.repair.broken_faces()` |

**requirements.txt for all mesh spaces:**
```
trimesh>=3.21.0
numpy>=1.26.0
Pillow>=10.0.0
gradio>=4.44.0
```

---

### Texture Utilities (7 Spaces)

| Space Name | CLI Command | Input | Output | Notes |
|-----------|-------------|-------|--------|-------|
| `AssetGen.texture.pbr` | `visual texture pbr` | Albedo PNG | 4 images: albedo, normal, roughness, metallic | Derive normal via Sobel; roughness = inverted grayscale; metallic = threshold. Use Pillow + numpy. |
| `AssetGen.texture.channel_pack` | `visual texture channel_pack` | 4 image uploads (R, G, B, A channels) | Packed RGBA PNG | `np.stack([r, g, b, a], axis=-1)` then Pillow |
| `AssetGen.texture.atlas_pack` | `visual texture atlas_pack` | Multiple image uploads + grid size dropdown | Atlas PNG | Arrange images in NxM grid with Pillow |
| `AssetGen.texture.mipmap` | `visual texture mipmap` | PNG upload | ZIP of mipmap chain (8 levels) | `image.resize(w//2, h//2, LANCZOS)` repeated |
| `AssetGen.texture.normalmap_convert` | `visual texture normalmap_convert` | Normal map PNG + direction toggle (DX→GL / GL→DX) | Converted normal map | Flip G channel: `img[:,:,1] = 255 - img[:,:,1]` |
| `AssetGen.texture.seamless` | `visual texture seamless` | PNG upload + blend width slider | Seamless-tiled PNG | Mirror edges and blend with original using alpha compositing |
| `AssetGen.texture.resize` | `visual texture resize` | PNG upload + width/height sliders + snap-to-pow2 checkbox | Resized PNG | `image.resize((w, h), Image.LANCZOS)` |
| `AssetGen.texture.report` | `visual texture report` | PNG upload | JSON report (size, channels, mode, estimated GPU VRAM at each mip) | PIL `image.info`, `image.mode`, compute VRAM as `w * h * channels * bytes_per_channel / 1024**2` |

**requirements.txt for all texture utility spaces:**
```
numpy>=1.26.0
Pillow>=10.0.0
gradio>=4.44.0
```

---

### Audio Processing (7 Spaces)

All audio process Spaces need `ffmpeg` installed system-wide for `pydub` to handle MP3/OGG.
Add to `packages.txt` (HF Spaces apt package installation):
```
ffmpeg
```

| Space Name | CLI Command | Input | Output | Key Package |
|-----------|-------------|-------|--------|-------------|
| `AssetGen.audio.process.normalize` | `audio process normalize` | WAV/MP3 upload + target LUFS slider (-23 to -6) | Normalized WAV | `pydub`, `pyloudnorm` |
| `AssetGen.audio.process.trim_silence` | `audio process trim_silence` | WAV upload + threshold slider | Trimmed WAV | `pydub` (`AudioSegment.strip_silence`) |
| `AssetGen.audio.process.convert` | `audio process convert` | Audio upload + format dropdown (WAV/OGG/MP3/FLAC) | Converted file | `pydub` |
| `AssetGen.audio.process.downmix` | `audio process downmix` | Stereo WAV + direction radio (stereo→mono / mono→stereo) | Remixed WAV | `pydub` |
| `AssetGen.audio.process.resample` | `audio process resample` | WAV + target sample rate dropdown (22050/44100/48000) | Resampled WAV | `pydub` or `scipy.io.wavfile` + `scipy.signal.resample` |
| `AssetGen.audio.process.loop_optimize` | `audio process loop_optimize` | WAV upload | WAV + loop point text (sample offsets for loop start/end) | `numpy`, `scipy` (zero-crossing search) |
| `AssetGen.audio.process.waveform` | `audio process waveform` | WAV upload | Waveform PNG | `numpy`, `matplotlib` |

**requirements.txt for audio process spaces:**
```
pydub>=0.25.1
pyloudnorm>=0.1.1
scipy>=1.13.0
matplotlib>=3.8.0
numpy>=1.26.0
gradio>=4.44.0
```

**packages.txt for audio process spaces:**
```
ffmpeg
```

---

### Remaining Procedural Generators (6 Spaces)

| Space Name | CLI Command | Input | Output | Notes |
|-----------|-------------|-------|--------|-------|
| `AssetGen.procedural.texture.noise` | `procedural texture noise` | Width/height sliders, noise type dropdown (Perlin/Worley/Value), scale, seed | PNG | Reuse noise functions from `AssetGen.procedural.terrain.heightmap` |
| `AssetGen.procedural.level.voronoi` | `procedural level voronoi` | Width/height sliders, N points slider, colormap dropdown, seed | PNG (Voronoi diagram) | `scipy.spatial.Voronoi` → render with Pillow |
| `AssetGen.procedural.foliage.scatter` | `procedural foliage scatter` | Area width/height, radius slider (minimum distance), seed | PNG scatter plot + CSV (x,y positions) | Poisson disk sampling with numpy |
| `AssetGen.procedural.tileset.wfc` | `procedural tileset wfc` | Upload tileset PNG (NxN grid of tiles) + adjacency rules (auto-detect or manual) + output size | Generated map PNG | WFC is complex; start with auto-detected adjacency from tile edges |
| `AssetGen.procedural.plant.lsystem` | `procedural plant lsystem` | L-system axiom text, rules (2–4 production rules), iterations slider, angle slider | PNG plant sketch | Turtle-style rendering with Pillow |
| `AssetGen.scene.physics.collider` | `scene physics collider` | GLB/OBJ upload + convex hull count slider | Convex hull mesh(es) GLB download | `trimesh.decomposition.convex_decomposition()` (wraps V-HACD if available, falls back to `trimesh.convex_hull`) |

**requirements.txt for procedural spaces:**
```
numpy>=1.26.0
scipy>=1.13.0
Pillow>=10.0.0
matplotlib>=3.8.0
trimesh>=3.21.0  # for physics collider space only
gradio>=4.44.0
```

---

### Remaining Visual Utility Spaces (6 Spaces)

| Space Name | CLI Command | Input | Output | Notes |
|-----------|-------------|-------|--------|-------|
| `AssetGen.lod.generate` | `visual lod generate` | GLB/OBJ upload + 3 target face-count sliders (LOD0/1/2) | 3 GLB files (LOD0, LOD1, LOD2) | `pyfqmr.Simplify` — `pip install pyfqmr` |
| `AssetGen.uv.auto` | `visual uv auto` | GLB/OBJ upload | GLB with auto-unwrapped UVs download | `xatlas` Python bindings — `pip install xatlas` |
| `AssetGen.vfx.particle` | `visual vfx particle` | Particle description Textbox + frame count + grid layout dropdown | PNG sprite sheet | SDXL (ZeroGPU) or pure Pillow for simple particles |
| `AssetGen.sprite.pack` | `visual sprite pack` | Multiple PNG uploads + cell size dropdown | Sprite sheet PNG + JSON manifest | Pillow grid packing + JSON with frame rects |
| `AssetGen.blockout.create` | `visual blockout create` | Text description of layout | Sketch-style overhead view PNG | SDXL with prompt prefix "top-down architect sketch, floor plan sketch, blueprint style" |
| `AssetGen.animate.mocap` | `visual animate mocap` | Image or short video upload | Annotated image/video with pose skeleton overlay | Already covered in Tier 2 (T2-8) |

**requirements.txt for LOD and UV spaces:**
```
pyfqmr>=0.2.0  # for lod.generate
xatlas>=0.0.9  # for uv.auto
trimesh>=3.21.0
numpy>=1.26.0
gradio>=4.44.0
```

---

### UI Variation Spaces (7 Spaces)

The following are all SDXL-based (ZeroGPU) variations on `AssetGen.concept.generate` and
`AssetGen.ui.icon`. The implementation agent should copy the `AssetGen.concept.generate` app.py
and modify only the system prompt prefix for each:

| Space Name | Prompt Prefix to Prepend |
|-----------|--------------------------|
| `AssetGen.ui.button` | `"game UI button element, stylized, {style_preset}, isolated on transparent background,"` |
| `AssetGen.ui.panel` | `"game UI panel/dialog box, {style_preset}, clean layout, game HUD element,"` |
| `AssetGen.ui.widget` | `"single game UI widget/control element, {style_preset}, isolated,"` |
| `AssetGen.ui.layout` | `"game UI screen layout wireframe, grid layout, {style_preset}, annotated design,"` |
| `AssetGen.ui.iconset` | `"set of 6 matching game icons on a grid, {style_preset}, themed icon sheet,"` |
| `AssetGen.ui.theme` | `"game UI theme style guide, color palette, {style_preset}, sample components,"` |
| `AssetGen.ui.screen` | `"complete game screen/menu design, {style_preset}, full layout with all UI elements,"` |

For all UI spaces, add a `style_preset` dropdown: Fantasy RPG | Sci-Fi | Minimalist | Retro Pixel | Horror | Cartoon.

**requirements.txt (same for all):**
```
diffusers>=0.28.0
transformers>=4.40.0
accelerate>=0.30.0
torch>=2.3.0
Pillow>=10.0.0
gradio>=4.44.0
```

---

### Narrative Validation Spaces (Low Priority — Optional)

These two Spaces are CPU-only and have low demo value, but can be useful as developer tools:

| Space Name | CLI Command | Input | Output | Notes |
|-----------|-------------|-------|--------|-------|
| `AssetGen.narrative.dialogue.validate` | `support narrative dialogue validate` | JSON text area (paste dialogue JSON) | Validation result (valid/invalid + error list) | `jsonschema` or custom AssetGen schema — import the schema from AssetGen or hardcode it |
| `AssetGen.narrative.quest.validate` | `support narrative quest validate` | JSON text area (paste quest graph JSON) | DAG validation result (cycles, unreachable nodes) | `networkx` for graph analysis |

---

## Full Tier 2 + 3 Creation Script

```bash
#!/usr/bin/env bash
set -e

# Tier 2
TIER2=(
  "assetgen.audio.ambient.generate"
  "assetgen.audio.voice.clone"
  "assetgen.audio.music.loop"
  "assetgen.model.multiview"
  "assetgen.model.splat"
  "assetgen.rig.auto"
  "assetgen.animate.keyframe"
  "assetgen.animate.mocap"
  "assetgen.concept.style"
  "assetgen.texture.inpaint"
  "assetgen.texture.from_concept"
  "assetgen.scene.lighting.hdri"
  "assetgen.narrative.lore.generate"
  "assetgen.narrative.quest.design"
  "assetgen.ui.icon"
  "assetgen.ui.mockup"
  "assetgen.procedural.level.dungeon"
)

# Tier 3 — mesh
TIER3_MESH=(
  "assetgen.mesh.validate"
  "assetgen.mesh.convert"
  "assetgen.mesh.bounds"
  "assetgen.mesh.center"
  "assetgen.mesh.scale"
  "assetgen.mesh.flipnormals"
  "assetgen.mesh.weld"
)

# Tier 3 — texture utilities
TIER3_TEXTURE=(
  "assetgen.texture.pbr"
  "assetgen.texture.channel_pack"
  "assetgen.texture.atlas_pack"
  "assetgen.texture.mipmap"
  "assetgen.texture.normalmap_convert"
  "assetgen.texture.seamless"
  "assetgen.texture.resize"
  "assetgen.texture.report"
)

# Tier 3 — audio processing
TIER3_AUDIO=(
  "assetgen.audio.process.normalize"
  "assetgen.audio.process.trim_silence"
  "assetgen.audio.process.convert"
  "assetgen.audio.process.downmix"
  "assetgen.audio.process.resample"
  "assetgen.audio.process.loop_optimize"
  "assetgen.audio.process.waveform"
)

# Tier 3 — procedural
TIER3_PROC=(
  "assetgen.procedural.texture.noise"
  "assetgen.procedural.level.voronoi"
  "assetgen.procedural.foliage.scatter"
  "assetgen.procedural.tileset.wfc"
  "assetgen.procedural.plant.lsystem"
  "assetgen.scene.physics.collider"
)

# Tier 3 — visual utilities
TIER3_VIS=(
  "assetgen.lod.generate"
  "assetgen.uv.auto"
  "assetgen.vfx.particle"
  "assetgen.sprite.pack"
  "assetgen.blockout.create"
)

# Tier 3 — UI variations
TIER3_UI=(
  "assetgen.ui.button"
  "assetgen.ui.panel"
  "assetgen.ui.widget"
  "assetgen.ui.layout"
  "assetgen.ui.iconset"
  "assetgen.ui.theme"
  "assetgen.ui.screen"
)

ALL=(
  "${TIER2[@]}"
  "${TIER3_MESH[@]}"
  "${TIER3_TEXTURE[@]}"
  "${TIER3_AUDIO[@]}"
  "${TIER3_PROC[@]}"
  "${TIER3_VIS[@]}"
  "${TIER3_UI[@]}"
)

for space in "${ALL[@]}"; do
  echo "Creating: $space"
  hf repo create "$space" --repo-type space --space-sdk gradio --exist-ok
done

echo "All Tier 2 + Tier 3 spaces created."
```
