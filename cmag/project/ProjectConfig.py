from __future__ import annotations
if __import__("typing").TYPE_CHECKING:
    from typing import Any, Dict, List
    from pathlib import Path

from pathlib import Path
from cmag.project.config import CMagConfig
from .ProjectConfigFields import CMagProjectConfigFields as configfields

class CMagProjectConfig(CMagConfig):

    def __init__(self, filepath, *args, **kwargs):
        self.filepath = Path(filepath)
        super().__init__(configfields, cfg_default=True, *args, **kwargs)

    def loadfile(self, **kwargs):
        self.load_from_file(self.filepath, **kwargs)

    def savefile(self, **kwargs):
        self.save_to_file(self.filepath, **kwargs)