from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    from typing import Any, Dict, List, Optional
    from cmag.project import CMagProject

from .model import CMagPluginModel

class CMagPluginManager:
    
    def __init__(self, project: CMagProject):

        self._project = project

        with self.project.db as database:
            CMagPluginModel.create_table()

    @property
    def project(self) -> CMagProject:
        return self._project

    def load_plugin_once(self, impfrom: str):
        pass

    def load_plugin(self, impfrom: str):
        pass

    def get_plugin(self, callname: str):
        pass

    def list_plugins(self):
        pass

    def save_plugin_options(self, callname: str):
        pass

    def unload_plugin_once(self, callname: str):
        pass

    def unload_plugin(self, callname: str):
        pass
