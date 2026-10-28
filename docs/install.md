# Installation & Upgrade

## Install

### Homebrew (macOS / Linux)

```bash
brew install aallbrig/tap/assetgen
```

### Chocolatey (Windows)

```powershell
choco install assetgen
```

### pip (all platforms)

```bash
pip install assetgen

# With GPU inference support (for the server machine)
pip install "assetgen[inference]"
```

### Windows with CUDA (server machine)

On a Windows machine with an NVIDIA GPU, install PyTorch with CUDA first:

```powershell
python -m venv C:\assetgen-venv
C:\assetgen-venv\Scripts\activate

# Install CUDA-enabled PyTorch, then assetgen
pip install torch --index-url https://download.pytorch.org/whl/cu121
pip install "assetgen[inference]"
```

See [Server Setup (Windows)](server-setup.md#quick-start-windows) for full details.

### From a GitHub Release

Each tagged release publishes a `.whl` wheel file on the
[Releases page](https://github.com/aallbrig/AssetGen/releases).

1. Go to [github.com/aallbrig/AssetGen/releases](https://github.com/aallbrig/AssetGen/releases)
2. Find the latest release (or the version you want)
3. Download the `.whl` file under **Assets**
4. Install it:

```bash
pip install assetgen-<version>-py3-none-any.whl

# With inference extras
pip install "assetgen-<version>-py3-none-any.whl[inference]"
```

### From source (development install)

```bash
git clone https://github.com/aallbrig/assetgen.git
cd assetgen
pip install -e ".[dev]"
```

---

## Upgrade

The easiest way to stay current is the built-in `upgrade` command:

```bash
# Check if a newer version exists, then prompt to upgrade
assetgen upgrade

# Just check — exit 0 if up-to-date, exit 1 if outdated (useful in scripts)
assetgen upgrade --check

# Upgrade without a confirmation prompt
assetgen upgrade --yes

# Include pre-releases
assetgen upgrade --pre
```

The `upgrade` command:

1. Fetches the latest release info from the GitHub Releases API
2. Compares it against the running version
3. If newer, shows a summary of the release notes
4. Runs `pip install AssetGen==<version>` in the same Python environment

!!! tip "Keeping inference extras"
    If you installed with `pip install "AssetGen[inference]"`, re-run with
    `pip install "AssetGen[inference]==<new-version>"` after upgrading, or add
    `--inference` support to the upgrade workflow in a future release.

---

## Verify installation

```bash
assetgen version
# assetgen  version: 0.0.1  python: 3.12.3  platform: Linux

assetgen --help
```

---

## Hardware recommendations

| GPU | VRAM | Suitable models |
|-----|------|----------------|
| RTX 4070 / 3080 | 12 GB | SDXL, TripoSR, MusicGen-Medium, AudioLDM2 |
| RTX 4090 / 3090 | 24 GB | All catalog models |
| Any CPU | — | Orchestration, job queue, text models |

Set the inference device in `~/.config/AssetGen/server.yaml`:

```yaml
device: "cuda"   # auto | cuda | cpu | mps (Apple Silicon)
```
