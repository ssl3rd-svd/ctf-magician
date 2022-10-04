from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    from typing import Any, Dict, List

import json
from pathlib import Path
from .ConfigField import CMagFieldTypes as fieldtypes

class CMagConfig:

    def __init__(self, fields: List[fieldtypes.default], cfg_path: Path, cfg_data: Dict[str, Any] = {}):

        self.fields = fields

        if cfg_data:
            with open(cfg_path, 'w') as f:
                json.dump(cfg_data, f)

        self.path = Path(cfg_path)
        self.data = {}
        self.load()
        self.save()

    def __del__(self):
        self.save()

    def __getitem__(self, key: str):
        for field in self.fields:
            if field.name == key:
                return field.get(self, field.OP_NONE, key=field.name)

    def __setitem__(self, key: str, value: Any):
        for field in self.fields:
            if field.name == key:
                return field.set(self, field.OP_NONE, key=field.name, value=value)

    @property
    def required_fields(self):
        return [field.name for field in self.fields if field.required]

    def load(self):

        with open(self.path) as f:
            loaded = json.load(f)

        for field in self.fields:
            field.set(self, field.OP_INIT, key=field.name, value=field.init)
            if field.required and field.name not in loaded:
                raise KeyError
            if field.name in loaded:
                self[field.name] = loaded[field.name]

    def save(self):

        to_save = {}

        for field in self.fields:
            key   = field.name
            value = field.get(self, field.OP_SAVE, key=field.name)
            to_save[key] = value

        with open(self.path, 'w') as f:
            json.dump(to_save, f)
