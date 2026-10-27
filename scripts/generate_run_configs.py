#!/usr/bin/env python3
"""
Generate PyCharm run configurations for all feasible HuggingFace Spaces.

Creates one XML file per Space in .idea/runConfigurations/, grouped into
domain folders for easy navigation in the Run Configurations dialog.

Usage:
    python scripts/generate_run_configs.py

Safe to re-run — files are overwritten idempotently.
When adding a new Space, add its entry to SPACES below and re-run.
"""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
RUNCONFIGS_DIR = REPO_ROOT / ".idea" / "runConfigurations"

# One entry per feasible Space: (space_repo_name, pycharm_folder_name)
# Folder names control the grouping in PyCharm's Run Configurations dialog.
SPACES: list[tuple[str, str]] = [
    # ── Audio (14) ───────────────────────────────────────────────────────────
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
    # ── Visual (43) ──────────────────────────────────────────────────────────
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
    # ── Scene (3) ────────────────────────────────────────────────────────────
    ("assetgen.scene.depth.estimate",         "Spaces: Scene"),
    ("assetgen.scene.lighting.hdri",          "Spaces: Scene"),
    ("assetgen.scene.physics.collider",       "Spaces: Scene"),
    # ── Procedural (7) ───────────────────────────────────────────────────────
    ("assetgen.procedural.terrain.heightmap", "Spaces: Procedural"),
    ("assetgen.procedural.texture.noise",     "Spaces: Procedural"),
    ("assetgen.procedural.level.dungeon",     "Spaces: Procedural"),
    ("assetgen.procedural.level.voronoi",     "Spaces: Procedural"),
    ("assetgen.procedural.foliage.scatter",   "Spaces: Procedural"),
    ("assetgen.procedural.tileset.wfc",       "Spaces: Procedural"),
    ("assetgen.procedural.plant.lsystem",     "Spaces: Procedural"),
    # ── Narrative (5) ────────────────────────────────────────────────────────
    ("assetgen.narrative.dialogue.npc",       "Spaces: Narrative"),
    ("assetgen.narrative.dialogue.validate",  "Spaces: Narrative"),
    ("assetgen.narrative.lore.generate",      "Spaces: Narrative"),
    ("assetgen.narrative.quest.design",       "Spaces: Narrative"),
    ("assetgen.narrative.quest.validate",     "Spaces: Narrative"),
]

_TEMPLATE = """\
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
            _TEMPLATE.format(space_name=space_name, folder=folder),
            encoding="utf-8",
        )
        created += 1
    print(f"Generated {created} run configurations → {RUNCONFIGS_DIR}")


if __name__ == "__main__":
    main()
