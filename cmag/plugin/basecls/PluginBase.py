from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cmag.project import CMagProject

from cmag.project.config import CMagConfig, CMagFieldTypes

class CMagPluginBase:

    name = ''
    config_fields = []

    def __init__(self, project: CMagProject):
        
        self._project = project

        if self.name == '':
            raise NotImplementedError

        if self.dir.is_dir():
            self._config = CMagConfig(self.config_fields, self.cfg_path)
        else:
            self.dir.mkdir()
            self._config = None

    @property
    def project(self):
        return self._project

    @property
    def dir(self):
        return self.project.plugins_dir / self.name

    @property
    def cfg_path(self):
        return self.dir / 'config.json'

    @property
    def config(self):
        return self._config

    def set_config(self, cfgval):
        self._config = CMagConfig(self.config_fields, self.cfg_path, cfgval)

    def start(self, *args, **kwargs):
        if self.config:
            self.run(*args, **kwargs)

    def check(self):
        raise NotImplementedError

    def run(self):
        raise NotImplementedError