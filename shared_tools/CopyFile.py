"""Copy a file from one absolute path to another.

This tool is used by multiple agents. Some agents may emit Linux-style `/mnt/...`
paths even when running on Windows outside Docker. On Windows, `/mnt/...` resolves
to `<drive>:\\mnt\\...`, which is *not* this repo's `./mnt` folder and can create
duplicate artifact trees. We normalize those inputs to the repo-local `./mnt`.
"""

import os
import shutil
from pathlib import Path

from agency_swarm.tools import BaseTool
from pydantic import Field

from slides_agent.tools.slide_file_utils import get_mnt_dir


def _normalize_mnt_path(p: str) -> str:
    raw = (p or "").strip()
    if not raw:
        return raw
    # Only needed for Windows non-docker runs.
    if os.name != "nt":
        return raw
    if Path("/.dockerenv").is_file():
        return raw

    # If the agent provides "/mnt/..." treat it as repo-local "./mnt/...".
    if raw.startswith("/mnt/") or raw == "/mnt":
        mnt = get_mnt_dir().resolve()
        suffix = raw[len("/mnt/") :] if raw.startswith("/mnt/") else ""
        return str(mnt / suffix)
    return raw


class CopyFile(BaseTool):
    """
    Copy a file from source_path to destination_path.

    Both paths must be absolute. The destination directory is created
    automatically if it does not exist. Use this to move uploaded user files
    (e.g. from the uploads folder) into a project's assets folder before
    referencing them in documents or slides.
    """

    source_path: str = Field(
        ...,
        description="Absolute path to the file to copy.",
    )
    destination_path: str = Field(
        ...,
        description="Absolute path where the file should be copied to (including filename).",
    )

    def run(self) -> str:
        src = Path(_normalize_mnt_path(self.source_path))
        dst = Path(_normalize_mnt_path(self.destination_path))

        if not src.exists():
            return f"Error: Source file not found: {src}"
        if not src.is_file():
            return f"Error: Source path is not a file: {src}"

        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)

        return f"Copied {src.name} to: {dst}"
