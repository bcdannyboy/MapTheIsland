"""Test-path bootstrap for local development before packaging is finalized."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE_ROOTS = (
    REPO_ROOT / "libs" / "schemas" / "src",
    REPO_ROOT / "libs" / "contracts" / "src",
    REPO_ROOT / "libs" / "policy" / "src",
)

for source_root in SOURCE_ROOTS:
    if str(source_root) not in sys.path:
        sys.path.insert(0, str(source_root))
