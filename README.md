# assetgen

AI-driven game asset generation pipeline — Kubernetes-style client/server architecture for 3D game development.

[![CI](https://github.com/aallbrig/assetgen/actions/workflows/ci.yml/badge.svg)](https://github.com/aallbrig/assetgen/actions/workflows/ci.yml)
[![Docs](https://img.shields.io/badge/docs-github.io-blue)](https://aallbrig.github.io/assetgen/)

📖 **[Full Documentation → aallbrig.github.io/assetgen](https://aallbrig.github.io/assetgen/)**

## Architecture

```
┌───────────────────────────────────────────────────────────┐
│  assetgen  (client CLI)                                      │
│  ├── visual model create --prompt "sword" --wait           │
│  ├── audio sfx generate "laser blast" --wait              │
│  └── jobs list / status / wait / cancel                   │
└───────────────────┬───────────────────────────────────────┘
                    │ HTTP (REST)
┌───────────────────▼───────────────────────────────────────┐
│  assetgen-server                                             │
│  ├── FastAPI REST API  (/jobs  /models  /health)          │
│  ├── WorkerThread      (polls SQLite queue)               │
│  ├── ModelManager      (HuggingFace Hub download/cache)   │
│  └── Validation        (allow-list + HF tag check)        │
└───────────────────┬───────────────────────────────────────┘
                    │
         ~/.config/assetgen/assetgen.db   (SQLite)
         ~/.local/share/assetgen/models/  (model cache)
```

The client auto-detects whether a server is configured:
- If `server_url` is set in `~/.config/assetgen/client.yaml` → use that server.
- Otherwise → start a local `assetgen-server` process (PID-tracked) and use it.

This lets you run the server on a powerful GPU machine and point your laptop's client at it, or just run everything locally.

## Installation

```bash
pip install assetgen

# For GPU inference (RTX 4070 recommended):
pip install "assetgen[inference]"
```

> **`[inference]` extra:** Installs `torch`, `transformers`, `diffusers`, `accelerate`, and
> `trimesh` for local GPU inference. Without it, assetgen is a fully functional client that can
> talk to a remote `assetgen-server`, but a local server will return stub outputs instead of
> running real models.
>
> For CI environments or machines without a GPU, `pip install assetgen` (without `[inference]`)
> is the right choice.

## Development Setup

Clone and run from source:

```bash
git clone https://github.com/aallbrig/assetgen.git
cd assetgen

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # Linux / macOS
# .venv\Scripts\activate         # Windows PowerShell

# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# For GPU inference (optional — needs CUDA-capable GPU):
pip install -e ".[dev,inference]"

# Verify the install
assetgen version
assetgen-server --help
```

Run tests: `pytest -v`  (or `make test`)

> **Version note:** assetgen uses `hatch-vcs` to derive its version from git tags.
> If you install without a git tag (fresh clone, no tags), the version will appear as `0.1.dev0`.
> Run `git tag v0.1.0` to set a version, or ignore the warning — it does not affect functionality.

## Quick Start

```bash
# Check version
assetgen version

# Start local server (optional — client auto-starts if not configured)
assetgen-server start --daemon

# Once the server is running, explore the REST API interactively:
# http://127.0.0.1:8432/docs      (Swagger UI)
# http://127.0.0.1:8432/redoc     (ReDoc)
# http://127.0.0.1:8432/health    (health check)

# Generate a 3D model
assetgen visual model create --prompt "low-poly medieval sword" --wait

# Generate sound effects
assetgen audio sfx generate "laser gun firing" --wait

# Generate background music
assetgen audio music compose "epic orchestral battle theme" --duration 30 --wait

# Auto-rig a character
assetgen visual rig auto character.glb --wait

# List recent jobs
assetgen jobs list

# Point client at a remote GPU server
assetgen client config set-server http://my-gpu-machine:8432

# View full game dev task → model catalog
assetgen tasks

# Show current server config
assetgen server config show
```

> **`assetgen-server` vs `assetgen server`:**
> - `assetgen-server start` — runs the inference server directly (the process itself)
> - `assetgen server start` — tells the client to launch a local `assetgen-server` process for you
> - `assetgen server status` / `assetgen server stop` — manage the locally auto-started server
>
> For a remote GPU machine, run `assetgen-server start --daemon` there, then on your laptop:
> `assetgen client config set-server http://<gpu-machine>:8432`

## CLI Command Tree

```
assetgen
├── tasks                     # View all game dev tasks and their assigned models
│   └── [--domain DOMAIN]     # filter by visual / audio / scene / pipeline / qa / support
├── visual                    # All 3D visual assets
│   ├── concept               # AI concept art (SDXL)
│   │   ├── generate          # text → concept art
│   │   ├── ref               # multi-view reference sheet
│   │   └── style             # art style samples
│   ├── blockout              # Greybox prototyping
│   │   ├── create            # text/image → blockout mesh
│   │   ├── assemble          # combine pieces into scene
│   │   └── iterate           # quick variation
│   ├── model                 # 3D mesh generation
│   │   ├── create            # text/image → .glb (TripoSR)
│   │   ├── highpoly          # high-poly refinement
│   │   ├── retopo            # auto-retopology
│   │   ├── splat             # Gaussian Splatting (3DGS)
│   │   ├── edit              # deform / boolean / combine
│   │   ├── optimize          # LOD generation
│   │   └── export            # convert to engine format
│   ├── uv                    # UV unwrapping
│   │   ├── auto              # AI smart-unwrap
│   │   ├── manual            # seam suggestions
│   │   └── optimize          # texel density optimisation
│   ├── texture               # PBR texturing & baking
│   │   ├── generate          # text → albedo + PBR maps
│   │   ├── apply             # project onto mesh
│   │   ├── bake              # high-to-low bake
│   │   └── pbr               # full PBR material set
│   ├── rig                   # Character rigging
│   │   ├── auto              # auto-skeleton (UniRig)
│   │   ├── skin              # skin weight maps
│   │   └── retarget          # rig retargeting
│   ├── animate               # Animation generation
│   │   ├── keyframe          # text → animation (AnimateDiff)
│   │   ├── mocap             # video → motion capture
│   │   ├── blend             # mix/loop animations
│   │   └── retarget          # animation retargeting
│   ├── vfx                   # VFX & particles
│   │   ├── particle          # particle sprite sheets
│   │   ├── decal             # dynamic decal textures
│   │   └── sim               # physics VFX bake
│   └── ui                    # UI/HUD elements
│       ├── icon              # icons & sprites
│       ├── hud               # health bars, minimaps
│       └── overlay           # 2D canvas overlays
├── audio                     # Sound & music
│   ├── sfx                   # Sound effects (AudioLDM2)
│   │   ├── generate          # text → WAV
│   │   ├── edit              # pitch/reverb/layer
│   │   └── library           # browse local SFX library
│   ├── music                 # Music (MusicGen)
│   │   ├── compose           # text → music track
│   │   ├── loop              # seamless loop generation
│   │   └── adaptive          # mood-based stems
│   └── voice                 # Voice synthesis (Bark)
│       ├── tts               # text → speech
│       ├── clone             # voice cloning
│       └── dialog            # batch NPC dialog
├── scene                     # Physics + lighting data
│   ├── physics               # Collision & simulation
│   │   ├── collider          # optimised collision mesh
│   │   ├── rigid             # rigid body setup
│   │   ├── cloth             # cloth/hair simulation bake
│   │   └── export            # engine physics export
│   └── lighting              # Lighting assets
│       ├── hdri              # text → HDR sky map
│       ├── probes            # reflection/irradiance probes
│       ├── volumetrics       # fog, clouds, atmosphere
│       └── bake              # GI lightmap bake
├── pipeline                  # Orchestration
│   ├── workflow              # Multi-step workflows
│   │   ├── create            # define step sequence
│   │   ├── run               # execute with inputs
│   │   └── list              # browse saved workflows
│   ├── batch                 # Batch processing
│   │   ├── queue             # enqueue from JSON manifest
│   │   ├── variant           # style/damage variants
│   │   └── status            # batch queue overview
│   └── integrate             # Engine integration
│       ├── export            # engine-specific export
│       ├── prefab            # bundle into prefab
│       └── script            # behavior stubs
├── support                   # Narrative & data
│   ├── narrative
│   │   ├── dialog            # NPC dialog trees
│   │   └── lore              # world-building text
│   └── data
│       ├── lightmap          # AI lightmap baking
│       └── proc              # procedural gen scripts
├── qa                        # Quality assurance
│   ├── validate              # mesh/UV/normal checks
│   ├── perf                  # polygon/VRAM analysis
│   ├── style                 # art style consistency
│   └── report                # full QA report
├── jobs                      # Job management
│   ├── list                  # list all jobs
│   ├── status <id>           # single job status (8-char prefix ok)
│   ├── wait <id>             # wait with progress bar
│   ├── cancel <id>           # cancel a job
│   └── clean                 # remove old jobs from DB
├── models                    # Model management
│   ├── list                  # catalog + install status
│   ├── status <id>           # single model details
│   └── install [id...]       # download from HuggingFace
├── config                    # Task → model catalog management
│   ├── list [--domain]       # browse all job types and their models
│   ├── show <job-type>       # detail for one job type
│   ├── set <job-type>        # set model for a job type (interactive HF search)
│   ├── remove <job-type>     # revert user override → built-in catalog
│   └── search <query>        # search HuggingFace for compatible models
├── client                    # Client-side configuration
│   └── config
│       ├── show              # show resolved server URL + health check
│       ├── set-server <url>  # point client at a remote server
│       └── unset-server      # revert to auto-start local server
└── server                    # Server management
    ├── start [--daemon]      # start local server
    ├── stop                  # stop local server
    ├── status                # server health check
    ├── config
    │   ├── show              # show all server settings
    │   ├── set <key> <val>   # persist a setting to server.yaml
    │   └── models [--domain] # view/manage task → model catalog
    ├── use <url>             # (alias for client config set-server)
    └── unset                 # (alias for client config unset-server)
```

## Configuration

Config lives in the OS-appropriate directory (XDG on Linux/macOS, `%APPDATA%` on Windows):

| File | Purpose |
|------|---------|
| `client.yaml` | Server URL, poll interval, default --wait |
| `server.yaml` | Host, port, device, security policy |
| `models.yaml` | User catalog overrides (task → HF model) |
| `assetgen.db` | SQLite job database |
| `server.pid` | Running local server PID |

```yaml
# ~/.config/assetgen/client.yaml
server_url: null          # null = auto-start local server
default_wait: false
poll_interval: 2.0

# ~/.config/assetgen/server.yaml
host: "127.0.0.1"
port: 8432
device: "auto"            # auto | cuda | cpu
log_level: "info"

# Security / model governance
allow_list: []            # [] = allow all models; restrict with a list:
                          # allow_list: ["stabilityai/TripoSR", "cvssp/audioldm2"]
skip_model_validation: false  # true = bypass HF pipeline_tag compatibility checks
```

## Task → Model Catalog

Every game-dev task maps to a HuggingFace model. The built-in catalog lives in
`src/assetgen/catalog.yaml`. Users can override any entry:

```bash
# Browse all tasks and their models
assetgen tasks

# Override the model for a task (interactive HF Hub search)
assetgen config set visual.model.create

# Or specify directly
assetgen config set visual.model.create --model-id stabilityai/TripoSR

# Revert to built-in
assetgen config remove visual.model.create
```

Client-side overrides are stored in `~/.config/assetgen/models.yaml` and sent
with each job submission (via the `model_id` field in the job request).

## Model Validation

When a job is submitted the server validates the requested model against the
task type using the HuggingFace Hub API:

1. **Allow-list check** — if `allow_list` is non-empty in `server.yaml`, only
   models on the list may be downloaded/used.
2. **Pipeline-tag check** — the model's `pipeline_tag` from HF Hub is checked
   against a compatibility table for the task (e.g., a TTS model will be
   rejected for `visual.model.create` which expects `image-to-3d`).

```bash
# Restrict downloads to approved models only
assetgen server config set allow_list '["stabilityai/TripoSR","cvssp/audioldm2"]'

# Trust all models (default)
assetgen server config set allow_list '[]'

# Skip compatibility checks (useful for research / experimental models)
assetgen server config set skip_model_validation true
```

When `skip_model_validation: false` (default) and the HF Hub API is
unreachable, the server **allows** the model (fail-open for offline use).

## Running as a systemd Service

```ini
# /etc/systemd/system/assetgen-server.service
[Unit]
Description=assetgen asset generation server
After=network.target

[Service]
Type=simple
User=youruser
ExecStart=/path/to/.venv/bin/assetgen-server start
Restart=on-failure
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

```bash
systemctl enable --now assetgen-server
journalctl -u assetgen-server -f   # follow JSON-structured logs
```

## Hardware Notes

- **RTX 4070 (12GB VRAM)**: Sufficient for SDXL, TripoSR, MusicGen-Medium, AudioLDM2
- Set `device: "cuda"` in `server.yaml` for GPU acceleration
- For lighter models, `device: "cpu"` works but is slower
- Use `HF_TOKEN` env var for authenticated Hub downloads (higher rate limits)

## Adding Real Inference Handlers

The worker dispatches each `job_type` to `assetgen/server/handlers/<job_type>.py`.
Create a module with a `run()` function:

```python
# src/assetgen/server/handlers/visual_model_create.py
from pathlib import Path
from typing import Any, Callable

def run(
    job_type: str,
    params: dict[str, Any],
    model_id: str | None,
    model_path: str | None,
    device: str,
    progress_cb: Callable[[float, str], None],
    output_dir: str,
) -> dict[str, Any]:
    progress_cb(0.2, "Loading model")
    # ... load transformers pipeline from model_path ...
    progress_cb(0.8, "Running inference")
    # ... write output files to output_dir ...
    return {
        "files": ["output.glb"],
        "metadata": {"model": model_id},
    }
```

Without a handler, jobs run through the stub handler (which simulates steps and returns immediately — useful for development).

## Contributing

PRs welcome. CI runs on every push/PR:
- `ruff check` — linting
- `pytest -v` — unit tests (no GPU required)

```bash
pip install -e ".[dev]"
ruff check src/ tests/
pytest -v
```

## Architecture

```
┌───────────────────────────────────────────────────────────┐
│  assetgen  (client CLI)                                      │
│  ├── visual model create --prompt "sword" --wait           │
│  ├── audio sfx generate "laser blast" --wait              │
│  └── jobs list / status / wait / cancel                   │
└───────────────────┬───────────────────────────────────────┘
                    │ HTTP (REST)
┌───────────────────▼───────────────────────────────────────┐
│  assetgen-server                                             │
│  ├── FastAPI REST API  (/jobs  /models  /health)          │
│  ├── WorkerThread      (polls SQLite queue)               │
│  └── ModelManager      (HuggingFace Hub download/cache)   │
└───────────────────┬───────────────────────────────────────┘
                    │
         ~/.config/assetgen/assetgen.db   (SQLite)
         ~/.local/share/assetgen/models/  (model cache)
```

The client auto-detects whether a server is configured:
- If `server_url` is set in `~/.config/assetgen/client.yaml` → use that server.
- Otherwise → start a local `assetgen-server` process (PID-tracked) and use it.

This lets you run the server on a powerful GPU machine and point your laptop's client at it, or just run everything locally.

## Installation

```bash
pip install assetgen

# For GPU inference (RTX 4070 recommended):
pip install "assetgen[inference]"
```

## Quick Start

```bash
# Check version
assetgen version

# Start local server (optional — client auto-starts if not configured)
assetgen-server start --daemon

# Generate a 3D model
assetgen visual model create --prompt "low-poly medieval sword" --wait

# Generate sound effects
assetgen audio sfx generate "laser gun firing" --wait

# Generate background music
assetgen audio music compose "epic orchestral battle theme" --duration 30 --wait

# Auto-rig a character
assetgen visual rig auto character.glb --wait

# List recent jobs
assetgen jobs list

# Point client at a remote server
assetgen server use http://my-gpu-machine:8432
```

## CLI Command Tree

```
assetgen
├── visual                    # All 3D visual assets
│   ├── concept               # AI concept art (SDXL)
│   │   ├── generate          # text → concept art
│   │   ├── ref               # multi-view reference sheet
│   │   └── style             # art style samples
│   ├── blockout              # Greybox prototyping
│   │   ├── create            # text/image → blockout mesh
│   │   ├── assemble          # combine pieces into scene
│   │   └── iterate           # quick variation
│   ├── model                 # 3D mesh generation
│   │   ├── create            # text/image → .glb (TripoSR)
│   │   ├── highpoly          # high-poly refinement
│   │   ├── retopo            # auto-retopology
│   │   ├── splat             # Gaussian Splatting (3DGS)
│   │   ├── edit              # deform / boolean / combine
│   │   ├── optimize          # LOD generation
│   │   └── export            # convert to engine format
│   ├── uv                    # UV unwrapping
│   │   ├── auto              # AI smart-unwrap
│   │   ├── manual            # seam suggestions
│   │   └── optimize          # texel density optimisation
│   ├── texture               # PBR texturing & baking
│   │   ├── generate          # text → albedo + PBR maps
│   │   ├── apply             # project onto mesh
│   │   ├── bake              # high-to-low bake
│   │   └── pbr               # full PBR material set
│   ├── rig                   # Character rigging
│   │   ├── auto              # auto-skeleton (UniRig)
│   │   ├── skin              # skin weight maps
│   │   └── retarget          # rig retargeting
│   ├── animate               # Animation generation
│   │   ├── keyframe          # text → animation (AnimateDiff)
│   │   ├── mocap             # video → motion capture
│   │   ├── blend             # mix/loop animations
│   │   └── retarget          # animation retargeting
│   ├── vfx                   # VFX & particles
│   │   ├── particle          # particle sprite sheets
│   │   ├── decal             # dynamic decal textures
│   │   └── sim               # physics VFX bake
│   └── ui                    # UI/HUD elements
│       ├── icon              # icons & sprites
│       ├── hud               # health bars, minimaps
│       └── overlay           # 2D canvas overlays
├── audio                     # Sound & music
│   ├── sfx                   # Sound effects (AudioLDM2)
│   │   ├── generate          # text → WAV
│   │   ├── edit              # pitch/reverb/layer
│   │   └── library           # browse local SFX library
│   ├── music                 # Music (MusicGen)
│   │   ├── compose           # text → music track
│   │   ├── loop              # seamless loop generation
│   │   └── adaptive          # mood-based stems
│   └── voice                 # Voice synthesis (Bark)
│       ├── tts               # text → speech
│       ├── clone             # voice cloning
│       └── dialog            # batch NPC dialog
├── scene                     # Physics + lighting data
│   ├── physics               # Collision & simulation
│   │   ├── collider          # optimised collision mesh
│   │   ├── rigid             # rigid body setup
│   │   ├── cloth             # cloth/hair simulation bake
│   │   └── export            # engine physics export
│   └── lighting              # Lighting assets
│       ├── hdri              # text → HDR sky map
│       ├── probes            # reflection/irradiance probes
│       ├── volumetrics       # fog, clouds, atmosphere
│       └── bake              # GI lightmap bake
├── pipeline                  # Orchestration
│   ├── workflow              # Multi-step workflows
│   │   ├── create            # define step sequence
│   │   ├── run               # execute with inputs
│   │   └── list              # browse saved workflows
│   ├── batch                 # Batch processing
│   │   ├── queue             # enqueue from JSON manifest
│   │   ├── variant           # style/damage variants
│   │   └── status            # batch queue overview
│   └── integrate             # Engine integration
│       ├── export            # engine-specific export
│       ├── prefab            # bundle into prefab
│       └── script            # behavior stubs
├── support                   # Narrative & data
│   ├── narrative
│   │   ├── dialog            # NPC dialog trees
│   │   └── lore              # world-building text
│   └── data
│       ├── lightmap          # AI lightmap baking
│       └── proc              # procedural gen scripts
├── qa                        # Quality assurance
│   ├── validate              # mesh/UV/normal checks
│   ├── perf                  # polygon/VRAM analysis
│   ├── style                 # art style consistency
│   └── report                # full QA report
├── jobs                      # Job management
│   ├── list                  # list all jobs
│   ├── status <id>           # single job status
│   ├── wait <id>             # wait with progress bar
│   ├── cancel <id>           # cancel a job
│   └── clean                 # remove old jobs from DB
├── models                    # Model management
│   ├── list                  # catalog + install status
│   ├── status <id>           # single model details
│   └── install [id...]       # download from HuggingFace
└── server                    # Server management
    ├── start [--daemon]       # start local server
    ├── stop                   # stop local server
    ├── status                 # server health check
    ├── config                 # show resolved config
    ├── use <url>              # point client at server
    └── unset                  # revert to auto-start
```

## Configuration

Config lives in the OS-appropriate directory (XDG on Linux/macOS, `%APPDATA%` on Windows):

| File | Purpose |
|------|---------|
| `client.yaml` | Server URL, poll interval, default --wait |
| `server.yaml` | Host, port, device (cuda/cpu), log level |
| `models.yaml` | User catalog overrides |
| `assetgen.db` | SQLite job database |
| `server.pid` | Running local server PID |

```yaml
# ~/.config/assetgen/client.yaml
server_url: null          # null = auto-start local server
default_wait: false
poll_interval: 2.0

# ~/.config/assetgen/server.yaml
host: "127.0.0.1"
port: 8432
device: "auto"            # auto | cuda | cpu
log_level: "info"
```

## Running as a systemd Service

```ini
# /etc/systemd/system/assetgen-server.service
[Unit]
Description=assetgen asset generation server
After=network.target

[Service]
Type=simple
User=youruser
ExecStart=/path/to/.venv/bin/assetgen-server start
Restart=on-failure
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

```bash
systemctl enable --now assetgen-server
journalctl -u assetgen-server -f   # follow JSON-structured logs
```

## Hardware Notes

- **RTX 4070 (12GB VRAM)**: Sufficient for SDXL, TripoSR, MusicGen-Medium, AudioLDM2
- Set `device: "cuda"` in `server.yaml` for GPU acceleration
- For lighter models, `device: "cpu"` works but is slower
- Use `HF_TOKEN` env var for authenticated Hub downloads (higher rate limits)

## Adding Real Inference Handlers

The worker dispatches each `job_type` to `assetgen/server/handlers/<job_type>.py`.
Create a module with a `run()` function:

```python
# src/assetgen/server/handlers/visual_model_create.py
from pathlib import Path
from typing import Any, Callable

def run(
    job_type: str,
    params: dict[str, Any],
    model_id: str | None,
    model_path: str | None,
    device: str,
    progress_cb: Callable[[float, str], None],
    output_dir: str,
) -> dict[str, Any]:
    progress_cb(0.2, "Loading model")
    # ... load transformers pipeline from model_path ...
    progress_cb(0.8, "Running inference")
    # ... write output files to output_dir ...
    return {
        "files": ["output.glb"],
        "metadata": {"model": model_id},
    }
```

Without a handler, jobs run through the stub handler (which simulates steps and returns immediately — useful for development).
