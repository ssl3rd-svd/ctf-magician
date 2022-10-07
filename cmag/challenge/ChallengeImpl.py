from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    from typing import Any, Dict, List

import shutil
import warnings
from pathlib import Path
from .ChallengeConfig import CMagChallengeConfig

class CMagChallengeImpl:
    
    def __init__(self, challenge_dir: str,
                       cfg_load_file: str = '',
                       cfg_load_dict: Dict[str, Any] = {},
                       cfg_load_default: bool = False,
                       cfg_save_on_init: bool = True):

        self._dir = challenge_dir
        self._cfg = CMagChallengeConfig(self.path_cfg, cfg_load_file, cfg_load_dict, cfg_load_default)

        if cfg_save_on_init:
            self.cfg.save()

    @property
    def dir(self) -> str:
        return str(self._dir)

    # Paths --

    @property
    def path(self) -> Path:
        (path := Path(self._dir)).mkdir(exist_ok=True)
        return path

    @property
    def path_cfg(self) -> Path:
        return self.path / 'config.json'

    @property
    def path_resources(self) -> Path:
        (path := self.path / 'resources').mkdir(exist_ok=True)
        return path

    # Objs --

    @property
    def cfg(self) -> CMagChallengeConfig:
        return self._cfg

    # File funcs --

    @property
    def files(self):
        return [self.get_file(p) for p in self.cfg['files']]

    def add_file(self, srcpath: str, relpath: str = '') -> str:

        abspath = self.path_resources / relpath
        if relpath not in self.cfg['files']:
            shutil.copyfile(srcpath, abspath)
            self.cfg['files'] += [relpath]
        else:
            warnings.warn(f'file exists: {abspath}')

        return str(abspath)

    def get_file(self, relpath: str = '') -> str | None:
        if relpath not in self.cfg['files']:
            return None
        if not (abspath := self.path_resources / relpath).is_file():
            return None
        return str(abspath)

    def remove_file(self, relpath: str):
        if (abspath := self.path_resources / relpath).is_file():
            abspath.unlink()

    # URL funcs --
    # TODO

    # SSH funcs --
    # TODO

    # Socket funcs --
    # TODO