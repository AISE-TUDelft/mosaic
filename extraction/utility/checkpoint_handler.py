"""Checkpoint persistence for resumable scraping."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict


class CheckpointHandler:
    """Simple JSON checkpoint helper for discovery/enrichment resume."""

    def __init__(self, path: Path) -> None:
        """Create a checkpoint handler bound to a JSON file path."""
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> Dict[str, Any]:
        """Load checkpoint state from disk if present."""
        if self.path.exists():
            try:
                with self.path.open("r", encoding="utf-8") as f:
                    data = json.load(f)
                if isinstance(data, dict):
                    print(f"[checkpoint] Loaded checkpoint from {self.path}")
                    return data
            except Exception:
                pass
        return {}

    def save(self, state: Dict[str, Any]) -> None:
        """Persist checkpoint state to disk."""
        try:
            with self.path.open("w", encoding="utf-8") as f:
                json.dump(state, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[checkpoint] Failed to save checkpoint: {e}")

    def clear(self) -> None:
        """Delete the checkpoint file if it exists."""
        try:
            if self.path.exists():
                self.path.unlink()
                print(f"[checkpoint] Cleared checkpoint at {self.path}")
        except Exception as e:
            print(f"[checkpoint] Failed to clear checkpoint: {e}")
