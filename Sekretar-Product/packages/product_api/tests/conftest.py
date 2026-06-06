from __future__ import annotations

import sys
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[2]
PRODUCT_API_SRC = PACKAGE_ROOT / "product_api" / "src"
IDENTITY_SRC = PACKAGE_ROOT / "identity" / "src"

sys.path.insert(0, str(PRODUCT_API_SRC))
sys.path.insert(0, str(IDENTITY_SRC))
