from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    from typing import Any, Dict, List, Optional
    from cmag.project import CMagProject

from .model import CMagPluginModel
from .option import CMagPluginOption

class CMagPlugin:

    optdef = CMagPluginOption

    def __init__(self, project: CMagProject, id: int):
        self._project = project
        self._id = id
        self._options = {}
        self.load_options()
    
    @property
    def project(self):
        return self._project

    @property
    def id(self):
        return self._id

    @property
    def options(self):
        return self._options

    def get_record(self):
        with self.project.db as database:
            return CMagPluginModel.get(CMagPluginModel.id == self.id)

    def load_options(self):
        if (record := self.get_record()) and record.options:
            self._options = self.optdef.from_json(record.options)
        return self._options

    def save_options(self):
        if self._options:
            options = self._options.to_json()
            self.get_record().update(options=options)

