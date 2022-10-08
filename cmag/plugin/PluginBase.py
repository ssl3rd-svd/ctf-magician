from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    from typing import Any, Dict, List
    from .PluginConfig import CMagPluginConfig

from pathlib import Path

class CMagPluginBase:

    callname: str = ''
    loaded: bool = False
    config: CMagPluginConfig = None

    def __init__(self, plugin_dir: str,
                       cfg_load_file: str = '',
                       cfg_load_dict: Dict[str, Any] = {},
                       cfg_load_default: bool = False,
                       cfg_save_on_init: bool = True):

        if self.callname == '':
            raise NotImplementedError
        if self.config == None:
            raise NotImplementedError

        self._dir = plugin_dir / self.callname
        self._cfg = self.config(self.path_cfg, cfg_load_file, cfg_load_dict, cfg_load_default)

        if cfg_save_on_init:
            self.cfg.save()

        self.loaded = True

    @property
    def dir(self) -> str:
        return self._dir

    # Paths --

    @property
    def path(self) -> Path:
        (path := Path(self.dir)).mkdir(exist_ok=True)
        return path

    @property
    def path_cfg(self) -> Path:
        return self.path / 'config.json'

    # Objs --

    @property
    def cfg(self) -> CMagPluginConfig:
        return self._cfg

    # Funcs --

    def save(self):
        self.cfg.save()

    # Virtual methods --

    def run(self, project=None, challenge=None, args=None, kwargs=None):
        raise NotImplementedError
