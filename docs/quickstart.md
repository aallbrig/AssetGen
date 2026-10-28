# Quick Start

This guide gets you from zero to generating your first 3D asset in about 5 minutes.

## 1. Install AssetGen

```bash
pip install "assetgen[inference]"
```

Verify:

```bash
assetgen --version
```

## 2. Start the server (optional)

The client **auto-starts** a local server on first use, so this step is optional.
If you want the server running in the background from the start:

```bash
assetgen-server start --daemon
assetgen server status
```

## 3. Check what tasks and models are available

```bash
assetgen tasks
```

This prints a full tree of every game-dev task alongside its assigned AI model:

```
🎮 assetgen — Game Asset Generation Pipeline
├── 🖼  Visual Assets
│   ├── 📐 3D Model Generation
│   │   ├── visual.model.create       [stabilityai/TripoSR]        Generate a 3D mesh...
│   │   ├── visual.model.splat        [huggingface/gaussian-...]   Gaussian Splatting...
...
```

Filter by domain:

```bash
assetgen tasks --domain audio
```

## 4. Generate your first asset

=== "One-liner (compose)"
    The fastest way to get a complete, game-ready asset is a **compose** command.
    One prompt, one command — the pipeline handles everything:

    ```bash
    # Complete static prop: concept → mesh → UV → texture → LODs → collider → export
    assetgen compose prop "wooden barrel, medieval dungeon" --engine godot --wait

    # Full PBR material set: albedo + normal + roughness + AO + metallic
    assetgen compose material "mossy cobblestone, wet" --wait

    # Level audio suite: ambient loop + music + 5 SFX
    assetgen compose soundscape "dungeon ambience, distant dripping" --wait
    ```

    See the [Compose Pipelines guide](compose-pipelines.md) for all commands.

=== "Individual steps"
    For finer control, run each step manually:
    ```bash
    # Generate a 3D prop (returns a job ID immediately)
    assetgen visual model create --prompt "low-poly medieval sword"

    # Or wait for it to complete
    assetgen visual model create --prompt "low-poly medieval sword" --wait
    ```

=== "Sound Effect"
    ```bash
    assetgen audio sfx generate "laser gun firing" --wait
    ```

=== "Music"
    ```bash
    assetgen audio music compose "epic orchestral battle theme" --duration 30 --wait
    ```

## 5. Track jobs

```bash
# List recent jobs
assetgen jobs list

# Check status (use the first 8 characters of the job ID)
assetgen jobs status a1b2c3d4

# Wait for a job with a live progress bar
assetgen jobs wait a1b2c3d4
```

## 6. Configure a model override

Each task uses a default model from the catalog. Override it for any task:

```bash
# Search HuggingFace interactively
assetgen config set visual.model.create

# Or specify directly
assetgen config set visual.model.create --model-id stabilityai/TripoSR

# Revert to built-in default
assetgen config remove visual.model.create
```

## 7. Point at a remote GPU server (optional)

If you have a desktop with a GPU, run `AssetGen-server` there and point your laptop at it.

**On the GPU machine** (Linux or Windows):

```bash
# Bind to all interfaces so LAN clients can connect
assetgen server config set host "0.0.0.0"

# Start the server
assetgen-server start --daemon
```

**On the client machine** (laptop):

```bash
# Point at the GPU machine (replace with its LAN IP)
assetgen client config set-server http://192.168.1.100:8432

# Verify connectivity
assetgen client config show    # should show "healthy"
```

If the health check fails, ensure:

- The server is running (`assetgen server status` on the GPU machine)
- Port 8432 is open (Windows Firewall / UFW — see [Server Setup](server-setup.md))
- Both machines are on the same network

**Pre-download recommended models** on the server to avoid long waits on first use:

```bash
assetgen models install --recommended
```

---

## What's next?

- [Compose Pipelines](compose-pipelines.md) — one command, complete asset pipelines
- [CLI Reference](cli-reference.md) — every command and option
- [Configuration](configuration.md) — server, client, and model catalog settings
- [Model Validation](model-validation.md) — allow-lists and HF pipeline-tag checks
- [Server Setup](server-setup.md) — systemd service, firewall, remote access
