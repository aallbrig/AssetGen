# Configuration

`AssetGen` uses plain YAML files stored under `~/.config/AssetGen/`.  All settings
have sane defaults so the tool works out-of-the-box without any manual
configuration.

---

## Files

| File | Who reads it | Purpose |
|------|--------------|---------|
| `~/.config/AssetGen/server.yaml` | `AssetGen-server` | Server behaviour, model allow-list |
| `~/.config/AssetGen/client.yaml` | `AssetGen` (client) | Server URL, output preferences |
| `~/.config/AssetGen/models.yaml` | Both | Override the built-in model catalog |

---

## server.yaml

```yaml
host: "127.0.0.1"      # Listen address
port: 8742             # TCP port
device: "auto"         # auto | cuda | mps | cpu
log_level: "INFO"

# If non-empty, only these model IDs can be downloaded/used.
# Empty list = allow everything.
allow_list: []

# Set true to skip the HuggingFace pipeline-tag compatibility check.
# The allow_list is ALWAYS enforced regardless of this setting.
skip_model_validation: false
```

Manage with:

```bash
assetgen server config show
assetgen server config set allow_list '["stabilityai/TripoSR"]'
assetgen server config set skip_model_validation true
```

---

## client.yaml

```yaml
server_url: null       # null = auto-start a local server
output_dir: "."        # Default output directory for generated files
```

Manage with:

```bash
assetgen client config show
assetgen client config set server_url "http://192.168.1.50:8742"
```

Setting `server_url` to a remote address means the client will never
auto-start a local server — useful when your GPU workstation runs the server
and you submit jobs from a laptop.

---

## models.yaml — User Catalog Overrides

Override any built-in model mapping by adding entries under the `catalog:` key:

```yaml
catalog:
  visual.model.create:
    model_id: "my-org/my-custom-triposr"
    name: "Custom TripoSR Fine-tune"
    task: "image-to-3d"
  audio.sfx.generate:
    model_id: "cvssp/audioldm2"
    name: "AudioLDM2"
    task: "text-to-audio"
```

Keys must exactly match a built-in job type (run `assetgen tasks` for the full
list).  After editing, restart the server — the catalog is loaded at startup.

---

## Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `ASSETGEN_CONFIG_DIR` | `~/.config/AssetGen` | Override the config directory |
| `ASSETGEN_DATA_DIR` | `~/.local/share/AssetGen` | Override the model cache root |
| `ASSETGEN_SERVER_URL` | *(from client.yaml)* | Runtime server URL override |
| `ASSETGEN_LOG_LEVEL` | `INFO` | Logging verbosity |
