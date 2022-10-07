from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    from typing import Any, Dict, List

import json
from pathlib import Path
from .ConfigField import CMagFieldTypes as fieldtypes

class CMagConfig:

    def __init__(self, fields: List[fieldtypes.default],
                       cfg_load_file: str | Path = {},
                       cfg_load_data: Dict[str, Any] = {},
                       cfg_load_default=False,
                       raise_key_error=True,
                       raise_value_error=True):

        self.fields = fields
        self.data = {}
        self.loaded = False

        if cfg_load_default:
            self.load_default()
        elif cfg_load_data:
            self.load(cfg_load_data, raise_key_error, raise_value_error)
        elif cfg_load_file:
            self.load_from_file(cfg_load_file, raise_key_error, raise_value_error)

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

    def load_default(self):
        for field in self.fields:
            field.set(self, field.OP_INIT, key=field.name, value=field.init)

    def load(self, config: Dict[str, Any], raise_key_error=True, raise_value_error=True):

        for field in self.fields:

            field.set(self, field.OP_INIT, key=field.name, value=field.init)

            if field.required:
                if field.name not in config and raise_key_error:
                    raise KeyError
                elif not config[field.name] and field.null and raise_value_error:
                    raise ValueError

            if field.name in config:
                self[field.name] = config[field.name]

        self.loaded = True

    def load_from_file(self, filepath, raise_key_error=True, raise_value_error=True):
        with open(filepath) as f:
            loaded = json.load(f)
            self.load(loaded, raise_key_error, raise_value_error)

    def save_to_file(self, filepath):

        to_save = {}

        for field in self.fields:
            key   = field.name
            value = field.get(self, field.OP_SAVE, key=field.name)
            to_save[key] = value

        with open(filepath, 'w') as f:
            json.dump(to_save, f)
