from __future__ import annotations
if __import__("typing").TYPE_CHECKING:
    from typing import Any, Dict, List
    from pathlib import Path

from cmag.project.config import CMagConfig
from cmag.project.config import CMagFieldTypes as fieldtypes

class plugins(fieldtypes.abspathlist):
    name = 'plugins'
    desc = 'External plugins path.'
    required = True

CMagProjectConfigFields = [plugins]

class CMagProjectConfig(CMagConfig):
    def __init__(self, cfg_path: Path, cfg_data: Dict[str, Any] = {}):
        CMagConfig.__init__(self, CMagProjectConfigFields, cfg_path, cfg_data)