import sys
from pathlib import Path


CHAPTER1_DEMO_ROOT = Path(__file__).resolve().parents[1] / "hello-agent" / "chapter1" / "first_agent"

sys.path.insert(0, str(CHAPTER1_DEMO_ROOT))
