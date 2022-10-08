from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    from typing import Any, Dict, List

import shutil
import warnings
from secrets import token_hex
from pathlib import Path
from cmag.challenge import CMagChallenge
from cmag.plugin import CMagPluginLoader
from .ProjectConfig import CMagProjectConfig

class CMagProjectImpl:

    def __init__(self, project_dir: str = '',
                       cfg_load_file: str = '',
                       cfg_load_dict: Dict[str, Any] = {},
                       cfg_load_default: bool = False,
                       cfg_save_on_init: bool = True):

        self._dir = project_dir
        self._cfg = CMagProjectConfig(self.path_cfg, cfg_load_file, cfg_load_dict, cfg_load_default)
        self._challenges: Dict[str, CMagChallenge] = {}
        self._loader = CMagPluginLoader(self.cfg['plugins'])

        if cfg_save_on_init:
            self.cfg.save()

    @property
    def dir(self) -> str:
        return self._dir

    # Paths --

    @property
    def path(self) -> Path:
        (path := Path(self._dir)).mkdir(exist_ok=True)
        return path

    @property
    def path_cfg(self) -> Path:
        return self.path / 'config.json'

    @property
    def path_challenges(self) -> Path:
        (path := self.path / 'challenges').mkdir(exist_ok=True)
        return path

    @property
    def path_plugins(self) -> Path:
        (path := self.path / 'plugins').mkdir(exist_ok=True)
        return path

    # Objs --

    @property
    def cfg(self) -> CMagProjectConfig:
        return self._cfg

    @property
    def challenges(self) -> Dict[str, CMagChallenge]:
        return self._challenges

    # Challenge methods --

    def add_challenge(self, cfg_load_file: str = '',
                            cfg_load_dict: Dict[str, Any] = {},
                            cfg_load_default: bool = False) -> CMagChallenge | None:

        for _ in range(32):

            dirname = token_hex(16)
            if dirname in self.cfg['challenges']:
                continue

            challenge_dir = self.path_challenges / dirname
            if challenge_dir.is_dir():
                continue

            break

        challenge = CMagChallenge.new(
            challenge_dir,
            cfg_load_file,
            cfg_load_dict,
            cfg_load_default
        )

        if challenge:
            self.cfg['challenges'] += [dirname]

        return self.load_challenge(dirname, cfg_load_file, cfg_load_dict, cfg_load_default)

    def load_challenge(self, dirname: str,
                             cfg_load_file: str = '',
                             cfg_load_dict: Dict[str, Any] = {},
                             cfg_load_default: bool = False) -> CMagChallenge | None:

        if dirname not in self.cfg['challenges']:
            warnings.warn(f'challenge not registered in current project.')

        if dirname in self.challenges and self.challenges[dirname]:
            return self.challenges[dirname]

        if not (challenge_path := self.path_challenges / dirname).is_dir():
            warnings.warn(f'challenge open failed')
            return None

        challenge = CMagChallenge.load(
            challenge_path,
            cfg_load_file,
            cfg_load_dict,
            cfg_load_default
        )

        if challenge:
            self.challenges[dirname] = challenge

        return challenge

    def unload_challenge(self):
        raise NotImplementedError

    def get_challenge(self, dirname: str) -> CMagChallenge | None:
        if dirname in self.cfg['challenges'] and dirname in self.challenges:
            return self.challenges[dirname]
        for dn in self.cfg['challenges']:
            if dn.startswith(dirname) and dn in self.challenges:
                return self.challenges[dn]

    def remove_challenge(self, dirname: str):

        if dirname in self.cfg['challenges']:
            self.cfg.remove(dirname)

        if dirname in self.challenges:
            del self.challenges[dirname]

        if (challenge_dir := self.path_challenges / dirname).is_dir():
            shutil.rmtree(challenge_dir, ignore_errors=True)

    # Plugin methods --

    def add_plugin(self):
        raise NotImplementedError

    def load_plugin(self):
        raise NotImplementedError

    def unload_plugin(self):
        raise NotImplementedError

    def get_plugin(self):
        raise NotImplementedError

    def remove_plugin(self):
        raise NotImplementedError
