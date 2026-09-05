from __future__ import annotations

import os
from pathlib import Path
import sys


def activate_candidate() -> Path:
    value = os.environ.get("CANDIDATE_ROOT")
    if not value:
        raise RuntimeError("CANDIDATE_ROOT must point to the frozen candidate fixture")
    root = Path(value).resolve()
    if not (root / "app").is_dir():
        raise RuntimeError(f"candidate root does not contain app/: {root}")
    sys.path.insert(0, str(root))
    os.chdir(root)
    return root
