from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cmag.project import CMagProject

from cmag.project.config import CMagConfig, CMagFieldTypes

class CMagPluginBase:

    name = ''
    config = None

    def __init__(self, project: CMagProject):
        
        self._project = project

        if self.name == '':
            raise NotImplementedError

        self._cfg = None

    @property
    def project(self):
        return self._project

    @property
    def dir(self):
        return self.project.plugins_dir / self.name

    @property
    def cfg(self):
        return self._cfg

    def start(self, *args, **kwargs):
        self.run(*args, **kwargs)

    def check(self):
        raise NotImplementedError

    def run(self):
        raise NotImplementedError