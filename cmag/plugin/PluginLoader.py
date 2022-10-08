from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    from typing import Any, Dict, List

import sys
import warnings
from pathlib import Path

from importlib import import_module
from .PluginBase import CMagPluginBase

class CMagPluginLoader:

    def __init__(self, plugin_modules: List[str], lazy_load=True, plugin_cfg_options={}):
        
        self._plugins: List[CMagPluginBase] = []
        self._loaded: List[CMagPluginBase] = []

        for module in plugin_modules:
            if (preloaded := self.import_plugin(module)):
                self._plugins += preloaded
            else:
                warnings.warn(f"failed to import plugin module: {module}")

        if lazy_load:
            return

        for plugin in self.plugins:

            if plugin.callname in plugin_cfg_options:
                cfg_options = plugin_cfg_options[plugin.callname]
            else:
                cfg_options = {}

            self.load(plugin.callname, **cfg_options)

    @property
    def plugins(self) -> List[CMagPluginBase]:
        return self._plugins

    @property
    def loaded(self) -> List[CMagPluginBase]:
        return self._loaded

    # Loader methods --

    def get_ctf_magician_plugins(self, module: Any) -> List[CMagPluginBase]:
        plugins = []
        for attrname in dir(module):
            attr = getattr(module, attrname)
            if attr == CMagPluginBase:
                continue
            if not issubclass(attr, CMagPluginBase):
                continue
            plugins.append(attr)
        return plugins

    def import_plugin(self, module_name: str) -> List[CMagPluginBase] | None:
        
        try:
            module = import_module(module_name)
        except ModuleNotFoundError:
            module = None

        if module:
            return self.get_ctf_magician_plugins(module)
        else:
            return self.import_plugin_by_path(module_name)

    def import_plugin_by_path(self, module_path: str) -> List[CMagPluginBase] | None:

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

        return self.get_ctf_magician_plugins(module)

    def load(self, plugin: CMagPluginBase,
                   plugin_dir: str = '',
                   cfg_load_file: str = '',
                   cfg_load_dict: Dict[str, Any] = {},
                   cfg_load_default: bool = False,
                   cfg_save_on_init: bool = True) -> CMagPluginBase | None:

        if plugin.loaded:
            warnings.warn(f"plugin '{plugin.callname}' already loaded.")
            return plugin

        loaded = plugin(plugin_dir, 
                        cfg_load_file, cfg_load_dict,
                        cfg_load_default, cfg_save_on_init)

        self._plugins.remove(plugin)
        self._plugins.append(loaded)
        return loaded

    def load_by_callname(self, callname: str,
                               plugin_dir: str = '',
                               **kwargs) -> CMagPluginBase | None:
        
        plugin = self.get_plugin(callname)
        return self.load(plugin, plugin_dir, **kwargs)

    # Plugin getters --

    def get_plugin(self, callname: str) -> CMagPluginBase | None:
        for plugin in self.plugins:
            if plugin.callname == callname:
                return plugin