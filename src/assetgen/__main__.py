"""Entry point for ``python -m assetgen``.

Allows the CLI to be invoked without the ``assetgen`` script being on PATH::

    python -m assetgen --help
    python -m assetgen gen visual model create --prompt "low-poly sword"
    python -m assetgen tasks
"""

from assetgen.client.cli import app

if __name__ == "__main__":
    app()
