# CLI Reference

The CLI reference below is **generated directly from the source code** — every
flag, argument, and help string you see here comes from the same Typer
annotations that power `assetgen --help`.  Any change to the code is immediately
reflected here on the next docs build.

## assetgen

::: mkdocs-typer
    :module: assetgen.client.cli
    :command: app
    :prog_name: assetgen
    :depth: 0



```
assetgen [OPTIONS] COMMAND
```

| Subcommand | Description |
|-----------|-------------|
| `compose` | **Multi-step asset pipelines** (NPC, weapon, prop, material, soundscape, ui-kit, environment) |
| `tasks` | Browse all game dev tasks and their assigned AI models |
| `visual` | 3D visual assets (models, textures, rigs, animations, VFX) |
| `audio` | Sound effects, music, and voice synthesis |
| `scene` | Physics collision data and lighting assets |
| `pipeline` | Workflows, batching, and engine integration |
| `support` | Narrative, lore, and procedural data |
| `qa` | Asset validation and performance testing |
| `jobs` | Job queue management |
| `models` | Model catalog and installation |
| `config` | Task → model catalog management |
| `client` | Client configuration (server targeting) |
| `server` | Server process management |
| `upgrade` | Check for and install the latest release |
| `version` | Print version information |

---

## assetgen compose

Multi-step asset pipelines — a single command that chains multiple generation steps
sequentially, passing each step's output into the next. The cost equals the sum of the
individual steps; there is no additional overhead.

### `assetgen compose npc`

Generate a complete game NPC from a text description:

```
concept art → multi-view (Zero123++) → mesh → UV unwrap → concept-guided texture
→ auto-rig (Unity humanoid) → animation retargeting → LOD levels → collision mesh
→ NPC dialog text → TTS voice lines → engine export
```

```bash
assetgen compose npc "pig shopkeeper with apron, medieval fantasy" --wait
assetgen compose npc "dark elf archer" --style "gritty realistic" --engine unreal --wait
assetgen compose npc "robot guard" --no-multiview \
    --animations idle,walk,attack_light,death \
    --skeleton humanoid --engine unity --wait
assetgen compose npc "wizard" --voice "elderly male, wise" --no-lod --no-collider --wait

# Preview what steps will run without executing
assetgen compose npc "dwarf warrior" --dry-run
```

| Flag | Default | Description |
|------|---------|-------------|
| `--style` | — | Visual style applied to all steps |
| `--voice` | — | TTS voice descriptor for dialog lines |
| `--animations` | `idle,walk,talk` | Comma-separated BVH clips to retarget |
| `--skeleton` | `humanoid` | `biped` or `humanoid` (Unity 55-bone naming) |
| `--engine` | `unity` | `unity` \| `unreal` \| `godot` |
| `--lod/--no-lod` | on | Generate LOD 0/1/2 |
| `--collider/--no-collider` | on | Generate collision mesh |
| `--multiview/--no-multiview` | on | Use Zero123++ for better mesh quality |
| `--quality` | `standard` | `draft` \| `standard` \| `high` |
| `--output` | — | Output directory |
| `--dry-run` | off | Print steps without executing |

### `assetgen compose weapon`

Generate a complete weapon asset:

```
concept art → mesh → UV unwrap → concept-guided texture → LOD levels
→ collision mesh → engine export
```

```bash
assetgen compose weapon "rusted iron longsword, dark fantasy" --wait
assetgen compose weapon "plasma rifle" --style "sci-fi, chrome" --engine unreal --wait
```

---

### `assetgen compose prop`

Generate a static game prop (barrel, crate, torch, furniture, etc.):

```
concept art → mesh → UV unwrap → concept-guided texture → LOD levels
→ collision mesh → engine export
```

```bash
assetgen compose prop "wooden barrel with iron bands, medieval" --wait
assetgen compose prop "stone pillar, dungeon" --type decoration --engine godot --wait
assetgen compose prop "lantern hanging, warm glow" --quality low --wait
assetgen compose prop "ornate chest, treasure" --dry-run
```

**Flags:**
- `--type {furniture,container,decoration,foliage,structure}` — steers the concept prompt
- `--quality {low,medium,high}` — mesh and texture quality
- `--engine {unity,unreal,godot}` — export format

---

### `assetgen compose material`

Generate a full PBR material set from a text description:

```
albedo texture → seamless tiling → normal map → PBR channels (roughness/AO/metallic)
→ optional upscale → engine export
```

Output: `albedo.png`, `normal.png`, `roughness.png`, `ao.png`, `metallic.png`

```bash
assetgen compose material "weathered cobblestone, mossy" --wait
assetgen compose material "rusted iron sheet" --resolution 2048 --upscale --wait
assetgen compose material "worn oak planks" --type wood --engine godot --wait
assetgen compose material "dragon scale skin, iridescent" --dry-run
```

**Flags:**
- `--resolution {512,1024,2048,4096}` — texture dimensions (default: 1024)
- `--upscale / --no-upscale` — 2× Real-ESRGAN pass (default: off)
- `--type {organic,metal,stone,wood,fabric}` — prompt augmentation
- `--engine {unity,unreal,godot}` — export folder structure

---

### `assetgen compose soundscape`

Generate a complete audio suite for a game level or biome:

```
ambient loop → theme music → loopable music → N themed SFX
→ loop optimization → export
```

```bash
assetgen compose soundscape "enchanted forest at night" --wait
assetgen compose soundscape "medieval tavern, busy crowd" --sfx-count 8 --wait
assetgen compose soundscape "dungeon" --sfx-list "drip,chain,growl,footstep" --wait
assetgen compose soundscape "space station" --no-music --duration 60 --wait
assetgen compose soundscape "volcano" --dry-run
```

**Flags:**
- `--sfx-count N` — number of SFX to generate (default: 5)
- `--sfx-list "a,b,c"` — explicit SFX prompts instead of auto-generated
- `--no-music` — skip music, generate ambient loop + SFX only
- `--duration N` — audio length in seconds (default: 30)

---

### `assetgen compose ui-kit`

Generate a cohesive UI element set for a game:

```
style reference → button states → dialog panel → N icons
→ widget elements → export
```

```bash
assetgen compose ui-kit "dark fantasy RPG" --wait
assetgen compose ui-kit "sci-fi HUD, blue glow" --icons "health,shield,ammo,radar" --wait
assetgen compose ui-kit "cozy farming game" --palette "warm earthy tones" --wait
assetgen compose ui-kit "horror survival" --dry-run
```

**Flags:**
- `--icons "a,b,c"` — comma-separated icon names to generate (default: health, mana, stamina, gold, sword, shield)
- `--palette "description"` — color palette hint added to every prompt
- `--engine {unity,unreal,godot}` — export folder structure

---

### `assetgen compose environment`

Generate a complete level environment kit — multiple props, ground material, and ambient audio — all sharing a common visual style:

```
style reference → N × (concept → mesh → UV → texture → LOD → collider)
→ ground material (albedo → seamless → normal → PBR)
→ ambient loop + theme music → batch export
```

```bash
assetgen compose environment "medieval tavern interior" --count 6 --wait
assetgen compose environment "sci-fi corridor" --count 4 --engine unreal --wait
assetgen compose environment "haunted forest clearing" \
    --items "dead tree,gravestone,iron fence,lantern" --wait
assetgen compose environment "crystal cave" --no-audio --no-ground --dry-run
```

**Flags:**
- `--count N` — number of props to generate (default: 6)
- `--items "a,b,c"` — explicit prop list (overrides `--count`)
- `--no-audio` — skip ambient and music generation
- `--no-ground` — skip ground material generation
- `--quality {low,medium,high}` — applied to all prop steps
- `--engine {unity,unreal,godot}` — export format

> **Note:** With 6 props this pipeline runs ~26 sequential steps. Use `--dry-run` to preview the full chain before submitting.

---

## assetgen pipeline

### `assetgen pipeline workflow`

Define and execute multi-step workflows. Unlike `compose`, workflows are saved as YAML
and can be parameterised at run-time. Each step waits for the previous to complete
and receives its output files as `upstream_files`.

```bash
# Define a workflow (auto-chains output → input by default)
assetgen pipeline workflow create my-npc \
    visual.concept.generate visual.model.splat visual.uv.auto visual.rig.auto

# Preview without executing
assetgen pipeline workflow run my-npc --dry-run

# Execute with custom inputs
assetgen pipeline workflow run my-npc --inputs '{"prompt": "pig shopkeeper"}'

# List saved workflows
assetgen pipeline workflow list
```

Workflow YAML format (saved to `~/.config/AssetGen/workflows/<name>.yaml`):

```yaml
name: my-npc
chain: true   # auto-pass upstream_files between steps
steps:
  - id: concept
    job_type: visual.concept.generate
  - id: mesh
    job_type: visual.model.splat
    from_step: concept        # receives concept's output as upstream_files
  - id: uv
    job_type: visual.uv.auto
    from_step: mesh
  - id: rig
    job_type: visual.rig.auto
    from_step: mesh
    params:
      skeleton: humanoid
```

---

## Global output flags

Three mutually exclusive output modes are available on every command:

| Flag | Description |
|------|-------------|
| _(default)_ | Rich human-readable output with colours and progress bars |
| `--json` | Emit machine-readable JSON to stdout; suppresses progress bars |
| `--yaml` | Emit machine-readable YAML to stdout; suppresses progress bars |

`--json` and `--yaml` are useful for scripting and piping to other tools:

```bash
# JSON — pipe to jq
assetgen --json gen visual concept generate "ruined castle" --wait | jq .job_id

# YAML — human-friendly alternative
assetgen --yaml jobs status a1b2c3d4

# Use in a pipeline
JOB=$(assetgen --json gen visual model create --wait | python -c "import sys,json; print(json.load(sys.stdin)['job_id'])")
assetgen --yaml jobs status "$JOB"
```

---

## assetgen tasks

```bash
assetgen tasks [--domain DOMAIN] [--json]
```

Displays a rich tree of all 82 game development tasks with their assigned AI models.

| Option | Description |
|--------|-------------|
| `--domain` | Filter by domain: `visual`, `audio`, `scene`, `pipeline`, `qa`, `support` |
| `--json` | Output as JSON for scripting |

---

## assetgen gen visual

### `assetgen gen visual model`

```bash
assetgen gen visual model create --prompt "medieval sword" [--input-image img.png] \
    [--format glb] [--model-id org/repo] [--wait]
assetgen gen visual model retopo input.glb [--target-faces 5000] [--wait]
assetgen gen visual model splat [--input-dir ./frames] [--wait]
assetgen gen visual model optimize input.glb [--lod-levels 3] [--wait]
assetgen gen visual model export input.glb [--engine unity|unreal|godot] [--wait]

# Multi-view turnaround: single image → 6 views (Zero123++) — better mesh quality
assetgen gen visual model multiview --input concept.png [--prompt "pig shopkeeper"] [--wait]
```

### `assetgen gen visual texture`

```bash
assetgen gen visual texture generate input.glb --prompt "worn leather" [--resolution 2048] [--wait]
assetgen gen visual texture bake high.glb low.glb [--map-types all] [--wait]
assetgen gen visual texture pbr input.glb [--style "sci-fi metal"] [--wait]

# Concept-guided texturing: style from concept art → UV texture atlas (IP-Adapter SDXL)
assetgen gen visual texture from-concept mesh.glb --concept concept.png \
    --prompt "pig shopkeeper, painterly" [--resolution 1024] [--wait]
```

### `assetgen gen visual rig`

```bash
assetgen gen visual rig auto character.glb [--skeleton humanoid|biped|animal|custom] [--wait]
# --skeleton humanoid  outputs Unity-compatible 55-bone naming (Hips, Spine, LeftUpperArm…)
assetgen gen visual rig skin character.glb [--bone-influence 4] [--wait]
assetgen gen visual rig retarget source.glb target.glb [--wait]
```

### `assetgen gen visual animate`

```bash
assetgen gen visual animate keyframe character.glb --prompt "walk cycle" [--frames 60] [--wait]
assetgen gen visual animate mocap video.mp4 [--target character.glb] [--wait]
assetgen gen visual animate blend anim1.glb anim2.glb [--weight 0.5] [--wait]

# BVH clip retargeting: apply bundled CMU Mocap clips to a rigged character
assetgen gen visual animate retarget rig.glb \
    --clips idle,walk,run,talk,attack_light,death \
    [--skeleton humanoid] [--wait]
# Available clips: idle, walk, run, turn_left, turn_right, talk, attack_light,
#                  attack_heavy, death, jump, strafe_left, strafe_right,
#                  crouch_idle, wave, sit_idle
```

### Other visual subcommands

```bash
assetgen gen visual concept generate --prompt "fantasy castle" [--wait]
assetgen gen visual uv auto mesh.glb [--wait]
assetgen gen visual vfx particle --prompt "fire explosion" [--wait]
```

### assetgen gen visual ui

Generate UI components for games — icons, HUD elements, and full screen compositions.

```bash
# Single items
assetgen gen visual ui icon    "health potion"         [--size 256] [--wait]
assetgen gen visual ui button  "medieval stone button" [--states normal,hover,pressed,focused] [--nine-slice auto] [--dpi 1x,2x] [--greyscale-base] [--wait]
assetgen gen visual ui panel   "gothic dialog frame"   [--type dialog] [--wait]
assetgen gen visual ui widget  "fantasy scroll health bar" [--type progressbar] [--wait]

# Screen-level compositions
assetgen gen visual ui mockup  "RPG main menu dark castle" [--reference sketch.png] [--wait]
assetgen gen visual ui layout  "sci-fi HUD, minimap top-right" [--reference grid.png] [--wait]
assetgen gen visual ui screen  "RPG combat HUD"        [--type gameplay] [--wait]

# Theme kits
assetgen gen visual ui iconset "fantasy RPG" --icons "sword,shield,potion,key" [--wait]
assetgen gen visual ui theme   "dark souls gothic stone" style_ref.png          [--wait]
```

---

## assetgen gen audio

```bash
assetgen gen audio sfx generate "laser gun firing" [--duration 2.0] [--model-id org/repo] [--wait]
assetgen gen audio music compose "epic battle theme" [--duration 30] [--wait]
assetgen gen audio music loop input.wav [--target-duration 60] [--wait]
assetgen gen audio voice tts "Welcome, hero." [--voice en_default] [--wait]
assetgen gen audio voice dialog dialog.json [--voice npcs.yaml] [--wait]
```

---

## assetgen jobs

```bash
assetgen jobs list [--status queued|running|completed|failed] [--limit 50]
assetgen jobs status <id>        # full 36-char UUID or 8-char prefix
assetgen jobs wait <id>          # block with live progress bar
assetgen jobs cancel <id>
assetgen jobs clean [--days 30]  # remove completed jobs older than N days
```

`jobs status` displays the job type, status, timestamps, **and the original user
input parameters** (prompt, flags, file paths) so you can review or reproduce
any previous run.  Pass `--json` / `--yaml` to get machine-readable output
suitable for re-running the job with tweaked parameters:

```bash
# Inspect a past run in YAML
assetgen --yaml jobs status a1b2c3d4

# Capture params and re-submit
assetgen --json jobs status a1b2c3d4 | jq .params
```

---

## assetgen models

```bash
assetgen models list [--domain DOMAIN] [--installed]
assetgen models status <model-id>
assetgen models install [model-id ...]   # download from HuggingFace
```

---

## assetgen config

Manages the task → HuggingFace model catalog. User overrides are saved to
`~/.config/AssetGen/models.yaml` and sent with each job submission.

```bash
assetgen config list [--domain DOMAIN] [--installed]
assetgen config show <job-type>
assetgen config set <job-type> [--model-id org/repo]   # interactive if no --model-id
assetgen config remove <job-type>                       # revert to built-in default
assetgen config search <query>                          # search HuggingFace
```

---

## assetgen client config

```bash
assetgen client config show              # show resolved server URL + live health check
assetgen client config set-server <url>  # point client at a remote server
assetgen client config unset-server      # revert to auto-start local server
```

---

## assetgen server config

```bash
assetgen server config show              # show all resolved server settings
assetgen server config set <key> <val>   # persist to ~/.config/assetgen/server.yaml
assetgen server config models [--domain] # view task → model catalog
```

### Configurable keys

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `host` | string | `127.0.0.1` | Bind address |
| `port` | int | `8432` | Listen port |
| `workers` | int | `1` | Concurrent worker threads |
| `device` | string | `auto` | `auto` / `cuda` / `cpu` / `mps` |
| `log_level` | string | `info` | Logging verbosity |
| `model_load_timeout` | int | `120` | Max seconds to wait for model download |
| `job_retention_days` | int | `30` | Days to keep completed jobs in DB |
| `allow_list` | list | `[]` | Allowed model IDs (`[]` = allow all) |
| `skip_model_validation` | bool | `false` | Bypass HF pipeline-tag compatibility check |

---

## assetgen server

```bash
assetgen server start [--daemon]    # start local assetgen-server
assetgen server stop                # stop local assetgen-server
assetgen server status              # check if server is healthy
assetgen server use <url>           # alias for: assetgen client config set-server
assetgen server unset               # alias for: assetgen client config unset-server
```

---

## assetgen upgrade

```bash
assetgen upgrade               # check and prompt to upgrade
assetgen upgrade --check       # exit 0 if up-to-date, exit 1 if outdated
assetgen upgrade --yes         # skip confirmation prompt
assetgen upgrade --pre         # include pre-release versions
```

---

## assetgen version

```bash
assetgen version
# assetgen  version: 0.0.1  python: 3.12.3  platform: Linux-6.8.0  build: v0.0.1-0-gabcdef0
```

---

## Global options

All commands support `--help`. The `--wait` / `-w` flag is available on all asset
generation commands and blocks until the job completes, showing a progress bar.

```bash
assetgen gen visual model create --help
assetgen gen audio sfx generate --help
```
