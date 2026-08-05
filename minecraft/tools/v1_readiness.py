from __future__ import annotations

# Legacy entry point retained for compatibility with local scripts.
# The active release classifier is v1_product_readiness.py, which gates only
# selected meaningful gameplay/progression mods rather than all manifest entries.
from v1_product_readiness import main


if __name__ == "__main__":
    raise SystemExit(main())
