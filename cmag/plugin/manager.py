from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    from typing import Any, Dict, List, Optional, Tuple
    from cmag.project import CMagProject

import sys
from importlib import import_module
from pathlib import Path
from cmag.plugin import CMagPlugin
from cmag.plugin.model import CMagPluginModel

class CMagPluginManager:


    def __init__(self, project: CMagProject):

        self._project = project
        with self.project.db as database:
            CMagPluginModel.create_table()

        self._plugins = []
        self.load_all()

    # properties

    @property
    def project(self) -> CMagProject:
        return self._project

    @property
    def plugins(self) -> List[CMagPlugin]:
        return self._plugins

    # methods

    def enable_plugin(self, id: int):
        with self.project.db as database:
            CMagPluginModel.get(CMagPluginModel.id == id).update(enabled=True)

    def disable_plugin(self, id: int):
        with self.project.db as database:
            CMagPluginModel.get(CMagPluginModel.id == id).update(enabled=False)

    def add_plugin(self, impfrom: str, options: dict = {}):
        
        # maybe we need to use exception-catch here? don't know...
        plugin = self.load_plugin_once(impfrom, options)
        self.unload_plugin_once(plugin.callname)

        with self.project.db as database:
            record = CMagPluginModel.create(impfrom=impfrom, options=plugin.options.to_json(), enabled=True)
            self.load_plugin(record=record)

    def load_all(self, clear=True) -> Tuple[int, int]:
        
        if clear:
            self._plugins = []

        loaded = 0
        total = 0

        with self.project.db as database:
            records = CMagPluginModel.select()
            total = len(records)
            for record in records:
                if self.load_plugin(record=record):
                    loaded += 1

        return (loaded, total)

    def load_plugin_once(self, impfrom: str, options: dict = {}) -> Optional[CMagPlugin]:

        plugin_class = CMagPluginManager.import_plugin(impfrom)
        if not plugin_class:
            return None

        plugin = plugin_class(self.project, -1, options)
        self.plugins.append(plugin)

        return plugin

    def load_plugin(self, id: int = -1, record: Any = None) -> Optional[CMagPlugin]:

        if not record:
            with self.project.db as database:
                record = CMagPluginModel.get(id=id)
                if not record:
                    return None

        if not record.enabled:
            return None

        plugin_class = CMagPluginManager.import_plugin(record.impfrom)
        if not plugin_class:
            return None

        plugin = plugin_class(self.project, record.id, record.options)
        self.plugins.append(plugin)
        return plugin

    def get_loaded_plugin(self, callname: str) -> Optional[CMagPlugin]:
        for plugin in self.plugins:
            if plugin.callname == callname:
                return plugin

    def list_plugins(self) -> Dict[int:str]:
        with self.project.db as database:
            return {plugin.id:plugin.impfrom for plugin in CMagPluginModel.select()}

    def list_loaded_plugins(self) -> List[CMagPlugin]:
        return self.plugins

    def save_loaded_plugin_options(self, callname: str):
        plugin = self.get_loaded_plugin(callname)
        plugin.save_options_to_db()

    def unload_plugin_once(self, callname: str):
        plugin = self.get_loaded_plugin(callname)
        self.plugins.remove(plugin)
        del plugin

    def unload_plugin(self, callname: str):
        raise NotImplementedError

    # static methods

    def get_plugin_from_module(module: Any) -> Optional[CMagPlugin]:
        for attrname in dir(module):
            attr = getattr(module, attrname)
            if attr == CMagPlugin:
                continue
            if not issubclass(attr, CMagPlugin):
                continue
            return attr

    def import_plugin_by_path(module_path: str) -> Optional[CMagPlugin]:

        target = Path(module_path)

        if target.name.endswith('.py'):
            name = target.stem
        else:
            name = target.name

        sys.path.append(target.parent)

        try:
            module = import_module(name)
        except ModuleNotFoundError:
            return None

        return CMagPluginManager.get_plugin_from_module(module)

    def import_plugin(module_name: str) -> Optional[CMagPlugin]:

        try:
            module = import_module(module_name)
        except ModuleNotFoundError:
            module = None

        if not module:
            return CMagPluginManager.import_plugin_by_path(module_name)

        return CMagPluginManager.get_plugin_from_module(module)
