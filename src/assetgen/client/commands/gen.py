"""``assetgen gen`` — all game-asset generation commands.

Every AI-driven generation task lives here, organised by domain:

.. code-block:: text

    assetgen gen visual concept generate   — concept art from text
    assetgen gen visual model create       — 3D mesh from text/image
    assetgen gen visual mesh validate      — mesh integrity check
    assetgen gen visual lod generate       — LOD mesh generation
    assetgen gen audio sfx generate        — sound effects from text
    assetgen gen audio process normalize   — audio normalization
    assetgen gen scene lighting hdri       — panoramic HDRI sky
    assetgen gen procedural terrain heightmap    — procedural heightmap
    assetgen gen procedural level dungeon        — BSP dungeon layout
    ...

See ``assetgen tasks`` for the full task tree with assigned models.
"""

from __future__ import annotations

import typer

from assetgen.client.commands.audio.music import app as music_app
from assetgen.client.commands.audio.process import app as process_app

# ── audio sub-apps ───────────────────────────────────────────────────────────
from assetgen.client.commands.audio.sfx import app as sfx_app
from assetgen.client.commands.audio.voice import app as voice_app

# ── support / pipeline / qa / proc sub-apps ───────────────────────────────────
from assetgen.client.commands.pipeline import app as pipeline_app
from assetgen.client.commands.procedural import app as proc_app
from assetgen.client.commands.qa import app as qa_app
from assetgen.client.commands.scene.lighting import app as lighting_app

# ── scene sub-apps ───────────────────────────────────────────────────────────
from assetgen.client.commands.scene.physics import app as physics_app
from assetgen.client.commands.support import app as support_app
from assetgen.client.commands.visual.animate import app as animate_app
from assetgen.client.commands.visual.blockout import app as blockout_app

# ── visual sub-apps ──────────────────────────────────────────────────────────
from assetgen.client.commands.visual.concept import app as concept_app
from assetgen.client.commands.visual.lod import app as lod_app
from assetgen.client.commands.visual.mesh import app as mesh_app
from assetgen.client.commands.visual.model import app as model_app
from assetgen.client.commands.visual.rig import app as rig_app
from assetgen.client.commands.visual.sprite import app as sprite_app
from assetgen.client.commands.visual.texture import app as texture_app
from assetgen.client.commands.visual.ui_cmd import app as ui_app
from assetgen.client.commands.visual.uv import app as uv_app
from assetgen.client.commands.visual.vfx import app as vfx_app

# ── visual ───────────────────────────────────────────────────────────────────
visual_app = typer.Typer(
    help="3D visual asset creation: models, textures, rigs, animations, VFX, UI.",
    no_args_is_help=True,
)
visual_app.add_typer(concept_app, name="concept", help="Concept art and style references")
visual_app.add_typer(blockout_app, name="blockout", help="Rapid greybox / blockout prototyping")
visual_app.add_typer(model_app, name="model", help="3D mesh generation, retopo, splat")
visual_app.add_typer(mesh_app, name="mesh", help="Mesh processing: validate, convert, repair")
visual_app.add_typer(lod_app, name="lod", help="LOD generation via QEM decimation")
visual_app.add_typer(uv_app, name="uv", help="UV unwrapping and layout optimisation")
visual_app.add_typer(texture_app, name="texture", help="PBR textures, baking, material sets")
visual_app.add_typer(sprite_app, name="sprite", help="Sprite sheet packing and animation frames")
visual_app.add_typer(rig_app, name="rig", help="Auto-rigging, skinning, retargeting")
visual_app.add_typer(animate_app, name="animate", help="Keyframe, mocap, and animation blending")
visual_app.add_typer(vfx_app, name="vfx", help="Particle systems, decals, simulations")
visual_app.add_typer(ui_app, name="ui", help="Icons, HUD elements, 2D overlays")


# ── audio ────────────────────────────────────────────────────────────────────
audio_app = typer.Typer(
    help="Sound effects, music, and voice synthesis.",
    no_args_is_help=True,
)
audio_app.add_typer(sfx_app, name="sfx", help="Sound effects generation")
audio_app.add_typer(music_app, name="music", help="Music and ambient track generation")
audio_app.add_typer(voice_app, name="voice", help="TTS, voice cloning, and dialog batching")
audio_app.add_typer(process_app, name="process", help="Audio processing: normalize, trim, convert")


# ── scene ────────────────────────────────────────────────────────────────────
scene_app = typer.Typer(
    help="Physics collision data and lighting assets.",
    no_args_is_help=True,
)
scene_app.add_typer(physics_app, name="physics", help="Colliders, rigid bodies, cloth sim")
scene_app.add_typer(lighting_app, name="lighting", help="HDRI skies, probes, lightmaps")


# ── top-level gen app ─────────────────────────────────────────────────────────
app = typer.Typer(
    name="gen",
    help=(
        "Generate game assets using AI models.\n\n"
        "Domains: visual · audio · scene · pipeline · procedural · support · qa\n\n"
        "Run 'assetgen tasks' for the full task tree with assigned models."
    ),
    no_args_is_help=True,
    rich_markup_mode=None,
)
app.add_typer(visual_app, name="visual", help="3D meshes, textures, rigs, animations, VFX, UI")
app.add_typer(audio_app, name="audio", help="Sound effects, music, voice synthesis")
app.add_typer(scene_app, name="scene", help="Physics colliders and lighting assets")
app.add_typer(
    pipeline_app, name="pipeline", help="Workflows, batching, engine integration, asset tools"
)
app.add_typer(
    proc_app, name="procedural", help="Procedural generation: terrain, levels, foliage, plants"
)
app.add_typer(support_app, name="support", help="Narrative, lore, procedural data")
app.add_typer(qa_app, name="qa", help="Asset validation and performance testing")
