from __future__ import annotations
import typing

if typing.TYPE_CHECKING:
    from typing import Any, Dict, List

import json
import warnings
from pathlib import Path
from cmag.utils.flatten import flatten, unflatten
from cmag.exception.ConfigExc import *

class CMagConfig:

    defaults = {}

    def __init__(self, filepath: str = '',
                       load_file: str = '',
                       load_dict: Dict[str, Any] = {},
                       load_default: bool = False):

        self.filepath = filepath
        self.config = None

        need_load = True

        if load_file and need_load:
            if self.load_file(load_file):
                need_load = False
            else:
                warnings.warn(f'failed to load file: {load_file}', CMagConfigWarning)

        if load_dict and need_load:
            if self.load_dict(load_dict):
                need_load = False
            else:
                warnings.warn(f'failed to load dict', CMagConfigWarning)

        if load_default and need_load:
            self.load_default()
            need_load = False

        if need_load and not self.load_file(filepath):
            warnings.warn(f'failed to load file: {load_file}', CMagConfigWarning)
            self.load_default()
            self.save()

    def load_dict(self, config: Dict[str, Any], defaults={}) -> bool:

        if not defaults:
            defaults = self.defaults

        for default_key in defaults:
            if not default_key in config:
                config[default_key] = defaults[default_key]

        self.config = unflatten(config)
        return True

    def load_file(self, filepath: str, raise_on_error=False) -> bool:

        try:
            with open(filepath) as f:
                config = json.load(f)
        except OSError as exc:
            if raise_on_error:
                raise CMagConfigLoadFailed(baseexc=exc)
            return False

        return self.load_dict(config)

    def load_default(self):
        self.config = self.defaults

    def save(self) -> bool:
        return self.save_as(self.filepath)

    def save_as(self, filepath: str, raise_on_error=False) -> bool:

        config = flatten(self.config)
        
        try:
            with open(filepath, 'w') as f:
                json.dump(config, f)
                
        except PermissionError as exc:
            if raise_on_error:
                raise CMagConfigSaveFailed(baseexc=exc)
            else:
                return False

        return True

    @property
    def items(self):
        return self.config.items

    @property
    def keys(self):
        return self.config.keys

    @property
    def values(self):
        return self.config.values

    def __getitem__(self, key):
        return self.config[key]

    def __setitem__(self, key, value):
        self.config[key] = value
        self.save()
