# PyCharm Run Configurations for HF Spaces

_Generated: 2026-04-11 13:15:00 UTC_

This document specifies the developer tooling that lets you open any Gradio Space in PyCharm
(or any JetBrains IDE with Python support) and run it with a single click — no terminal required.

---

## 1. What Gets Created and Where

```
.idea/
└── runConfigurations/
    ├── space_AssetGen_audio_sfx_generate.xml      # Space: assetgen.audio.sfx.generate
    ├── space_AssetGen_audio_music_compose.xml
    ├── ...                                       # 72 total — one per feasible Space
    └── space_AssetGen_ui_screen.xml
```

Each XML file is a standard PyCharm Python run configuration. Opening the project in
PyCharm shows all 72 configurations pre-populated under "Run > Edit Configurations",
organised into five domain folders.

---

## 2. `.gitignore` Allowlist

The repo's `.gitignore` normally ignores the entire `.idea/` directory. An allowlist
block tracks only the run configuration XMLs, keeping all other IDE-local files private:

```gitignore
# IDE — ignore all of .idea except tracked run configurations
.idea/*
!.idea/runConfigurations/
.idea/runConfigurations/*
!.idea/runConfigurations/*.xml
```

This is already applied. The six existing non-Space configurations (`AssetGen_cli.xml`,
`AssetGen_server.xml`, `pytest_all_tests.xml`, etc.) are also tracked under the same rule.

---

## 3. Domain Folder Groups

Configurations are assigned to named folders for navigation in the Run Configurations dialog:

| PyCharm Folder | Spaces |
|---|---|
| `Spaces: Audio` | 14 audio generation + processing spaces |
| `Spaces: Visual` | 43 concept, texture, 3D, mesh, rig, animate, UI, sprite spaces |
| `Spaces: Scene` | 3 depth, lighting, physics spaces |
| `Spaces: Procedural` | 7 terrain, noise, dungeon, WFC, L-system spaces |
| `Spaces: Narrative` | 5 dialogue, lore, quest spaces |

---

## 4. Configuration Properties

Every Space run configuration uses the same settings, matching the project's existing
run config style:

| Property | Value |
|---|---|
| Type | Python |
| Module | `AssetGen` (uses project SDK = `.venv`) |
| Working directory | `$PROJECT_DIR$/spaces/<space-name>/` |
| Script | `$PROJECT_DIR$/spaces/<space-name>/app.py` |
| `EMULATE_TERMINAL` | `true` (so the Gradio URL prints in the console pane) |
| `PYTHONUNBUFFERED` | `1` |
| `IS_MODULE_SDK` | `true` (inherits project `.venv`) |

---

## 5. XML Template

When adding a new Space (e.g. after a new command is added to AssetGen), create its run
config by copying this template to `.idea/runConfigurations/space_<name_with_underscores>.xml`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<component name="ProjectRunConfigurationManager">
  <configuration default="false"
                 name="Space: assetgen.<domain>.<command>"
                 type="PythonConfigurationType"
                 factoryName="Python"
                 folderName="Spaces: <Domain>">
    <module name="assetgen" />
    <option name="INTERPRETER_OPTIONS" value="" />
    <option name="PARENT_ENVS" value="true" />
    <envs>
      <env name="PYTHONUNBUFFERED" value="1" />
    </envs>
    <option name="SDK_HOME" value="" />
    <option name="WORKING_DIRECTORY" value="$PROJECT_DIR$/spaces/assetgen.<domain>.<command>" />
    <option name="IS_MODULE_SDK" value="true" />
    <option name="ADD_CONTENT_ROOTS" value="true" />
    <option name="ADD_SOURCE_ROOTS" value="true" />
    <EXTENSION ID="PythonCoverageRunConfigurationExtension" runner="coverage.py" />
    <option name="SCRIPT_NAME" value="$PROJECT_DIR$/spaces/assetgen.<domain>.<command>/app.py" />
    <option name="PARAMETERS" value="" />
    <option name="SHOW_COMMAND_LINE" value="false" />
    <option name="EMULATE_TERMINAL" value="true" />
    <option name="MODULE_MODE" value="false" />
    <option name="REDIRECT_INPUT" value="false" />
    <option name="INPUT_FILE" value="" />
    <method v="2" />
  </configuration>
</component>
```

**Filename convention:** replace every `.` in the Space name with `_` and prefix with `space_`:
`AssetGen.audio.sfx.generate` → `space_AssetGen_audio_sfx_generate.xml`

---

## 6. Generating Run Configs in Bulk

When implementing a new batch of Spaces, regenerate all XMLs at once using this script
(safe to re-run — it overwrites existing files idempotently):

```bash
python scripts/generate_run_configs.py
```

This script lives at `scripts/generate_run_configs.py` and reads the list of feasible
Spaces from `AssetGen.catalog` (all_job_types) cross-referenced with the feasibility matrix.
See Section 7 for the script source.

Alternatively, run the inline generator directly:

```bash
python3 - <<'EOF'
import os
RUNCONFIGS_DIR = ".idea/runConfigurations"
SPACES = [
    # paste the SPACES list from the agent briefing Section 5 / Phase 0.8
]
TEMPLATE = """..."""  # paste template from Section 5 above
for space_name, folder in SPACES:
    filename = "space_" + space_name.replace(".", "_") + ".xml"
    with open(os.path.join(RUNCONFIGS_DIR, filename), "w") as f:
        f.write(TEMPLATE.format(space_name=space_name, folder=folder))
EOF
```

---

## 7. `scripts/generate_run_configs.py` Spec

Create this file alongside `scripts/sync_spaces.py`. It should be callable standalone:

```python
#!/usr/bin/env python3
"""
Generate PyCharm run configurations for all HuggingFace Spaces.

Usage:
    python scripts/generate_run_configs.py

Safe to re-run — existing files are overwritten idempotently.
"""
from __future__ import annotations
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
RUNCONFIGS_DIR = REPO_ROOT / ".idea" / "runConfigurations"

# One entry per feasible Space: (space_repo_name, pycharm_folder_name)
SPACES: list[tuple[str, str]] = [
    # Audio (14)
    ("assetgen.audio.sfx.generate",           "Spaces: Audio"),
    ("assetgen.audio.music.compose",          "Spaces: Audio"),
    ("assetgen.audio.music.loop",             "Spaces: Audio"),
    ("assetgen.audio.music.adaptive",         "Spaces: Audio"),
    ("assetgen.audio.ambient.generate",       "Spaces: Audio"),
    ("assetgen.audio.voice.tts",              "Spaces: Audio"),
    ("assetgen.audio.voice.clone",            "Spaces: Audio"),
    ("assetgen.audio.process.normalize",      "Spaces: Audio"),
    ("assetgen.audio.process.trim_silence",   "Spaces: Audio"),
    ("assetgen.audio.process.loop_optimize",  "Spaces: Audio"),
    ("assetgen.audio.process.convert",        "Spaces: Audio"),
    ("assetgen.audio.process.downmix",        "Spaces: Audio"),
    ("assetgen.audio.process.resample",       "Spaces: Audio"),
    ("assetgen.audio.process.waveform",       "Spaces: Audio"),
    # Visual (43)
    ("assetgen.concept.generate",             "Spaces: Visual"),
    ("assetgen.concept.style",                "Spaces: Visual"),
    ("assetgen.blockout.create",              "Spaces: Visual"),
    ("assetgen.model.create",                 "Spaces: Visual"),
    ("assetgen.model.multiview",              "Spaces: Visual"),
    ("assetgen.model.splat",                  "Spaces: Visual"),
    ("assetgen.mesh.validate",                "Spaces: Visual"),
    ("assetgen.mesh.convert",                 "Spaces: Visual"),
    ("assetgen.mesh.merge",                   "Spaces: Visual"),
    ("assetgen.mesh.bounds",                  "Spaces: Visual"),
    ("assetgen.mesh.flipnormals",             "Spaces: Visual"),
    ("assetgen.mesh.weld",                    "Spaces: Visual"),
    ("assetgen.mesh.center",                  "Spaces: Visual"),
    ("assetgen.mesh.scale",                   "Spaces: Visual"),
    ("assetgen.lod.generate",                 "Spaces: Visual"),
    ("assetgen.uv.auto",                      "Spaces: Visual"),
    ("assetgen.texture.generate",             "Spaces: Visual"),
    ("assetgen.texture.upscale",              "Spaces: Visual"),
    ("assetgen.texture.from_concept",         "Spaces: Visual"),
    ("assetgen.texture.inpaint",              "Spaces: Visual"),
    ("assetgen.texture.pbr",                  "Spaces: Visual"),
    ("assetgen.texture.channel_pack",         "Spaces: Visual"),
    ("assetgen.texture.convert",              "Spaces: Visual"),
    ("assetgen.texture.atlas_pack",           "Spaces: Visual"),
    ("assetgen.texture.mipmap",               "Spaces: Visual"),
    ("assetgen.texture.normalmap_convert",    "Spaces: Visual"),
    ("assetgen.texture.seamless",             "Spaces: Visual"),
    ("assetgen.texture.resize",               "Spaces: Visual"),
    ("assetgen.texture.report",               "Spaces: Visual"),
    ("assetgen.rig.auto",                     "Spaces: Visual"),
    ("assetgen.animate.keyframe",             "Spaces: Visual"),
    ("assetgen.animate.mocap",                "Spaces: Visual"),
    ("assetgen.vfx.particle",                 "Spaces: Visual"),
    ("assetgen.sprite.pack",                  "Spaces: Visual"),
    ("assetgen.ui.icon",                      "Spaces: Visual"),
    ("assetgen.ui.button",                    "Spaces: Visual"),
    ("assetgen.ui.panel",                     "Spaces: Visual"),
    ("assetgen.ui.widget",                    "Spaces: Visual"),
    ("assetgen.ui.mockup",                    "Spaces: Visual"),
    ("assetgen.ui.layout",                    "Spaces: Visual"),
    ("assetgen.ui.iconset",                   "Spaces: Visual"),
    ("assetgen.ui.theme",                     "Spaces: Visual"),
    ("assetgen.ui.screen",                    "Spaces: Visual"),
    # Scene (3)
    ("assetgen.scene.depth.estimate",         "Spaces: Scene"),
    ("assetgen.scene.lighting.hdri",          "Spaces: Scene"),
    ("assetgen.scene.physics.collider",       "Spaces: Scene"),
    # Procedural (7)
    ("assetgen.procedural.terrain.heightmap", "Spaces: Procedural"),
    ("assetgen.procedural.texture.noise",     "Spaces: Procedural"),
    ("assetgen.procedural.level.dungeon",     "Spaces: Procedural"),
    ("assetgen.procedural.level.voronoi",     "Spaces: Procedural"),
    ("assetgen.procedural.foliage.scatter",   "Spaces: Procedural"),
    ("assetgen.procedural.tileset.wfc",       "Spaces: Procedural"),
    ("assetgen.procedural.plant.lsystem",     "Spaces: Procedural"),
    # Narrative (5)
    ("assetgen.narrative.dialogue.npc",       "Spaces: Narrative"),
    ("assetgen.narrative.dialogue.validate",  "Spaces: Narrative"),
    ("assetgen.narrative.lore.generate",      "Spaces: Narrative"),
    ("assetgen.narrative.quest.design",       "Spaces: Narrative"),
    ("assetgen.narrative.quest.validate",     "Spaces: Narrative"),
]

TEMPLATE = """\
<?xml version="1.0" encoding="UTF-8"?>
<component name="ProjectRunConfigurationManager">
  <configuration default="false" name="Space: {space_name}" type="PythonConfigurationType" factoryName="Python" folderName="{folder}">
    <module name="assetgen" />
    <option name="INTERPRETER_OPTIONS" value="" />
    <option name="PARENT_ENVS" value="true" />
    <envs>
      <env name="PYTHONUNBUFFERED" value="1" />
    </envs>
    <option name="SDK_HOME" value="" />
    <option name="WORKING_DIRECTORY" value="$PROJECT_DIR$/spaces/{space_name}" />
    <option name="IS_MODULE_SDK" value="true" />
    <option name="ADD_CONTENT_ROOTS" value="true" />
    <option name="ADD_SOURCE_ROOTS" value="true" />
    <EXTENSION ID="PythonCoverageRunConfigurationExtension" runner="coverage.py" />
    <option name="SCRIPT_NAME" value="$PROJECT_DIR$/spaces/{space_name}/app.py" />
    <option name="PARAMETERS" value="" />
    <option name="SHOW_COMMAND_LINE" value="false" />
    <option name="EMULATE_TERMINAL" value="true" />
    <option name="MODULE_MODE" value="false" />
    <option name="REDIRECT_INPUT" value="false" />
    <option name="INPUT_FILE" value="" />
    <method v="2" />
  </configuration>
</component>
"""


def main() -> None:
    RUNCONFIGS_DIR.mkdir(parents=True, exist_ok=True)
    created = 0
    for space_name, folder in SPACES:
        filename = "space_" + space_name.replace(".", "_") + ".xml"
        path = RUNCONFIGS_DIR / filename
        path.write_text(
            TEMPLATE.format(space_name=space_name, folder=folder),
            encoding="utf-8",
        )
        created += 1
    print(f"Generated {created} run configurations in {RUNCONFIGS_DIR}")


if __name__ == "__main__":
    main()
```

---

## 8. When to Re-run

- **Now:** All 72 XMLs are already created and tracked in git.
- **After adding a new Space:** Add its entry to `SPACES` in `generate_run_configs.py`
  and re-run the script. Commit the new XML.
- **After removing a Space:** Remove its entry and delete the XML manually, then commit.
- **Never edit the XMLs by hand** — use the script to keep the SPACES list as the
  single source of truth.

---

## 9. Usage in PyCharm

1. Open the project root in PyCharm (File > Open > `/path/to/AssetGen`)
2. PyCharm detects the `.venv` and sets it as the project SDK automatically
3. Open "Run > Edit Configurations" (or the run selector dropdown at the top)
4. Find the `Spaces: Audio`, `Spaces: Visual`, etc. folders
5. Select any Space and click Run (▶) — Gradio opens at `http://127.0.0.1:7860`

> **Note:** If `spaces/AssetGen.X/app.py` does not exist yet (Space not implemented),
> PyCharm shows a "Script file not found" warning. The run config is still valid —
> it just needs the implementation file to exist before it can execute.
