from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    from typing import Any, Dict, List, Tuple, Optional
    from cmag.plugin import CMagPlugin

import json
from playhouse.shortcuts import model_to_dict
from cmag.plugin.model import CMagPluginModel
from cmag.plugin.manager_impl import CMagPluginManagerImpl

class CMagPluginManager(CMagPluginManagerImpl):

    def __repr__(self) -> str:
        return f"<CMagPluginManager loaded={len(self.list_loaded_plugins())}>"

    def load_all(self, clear=True) -> Tuple[int, int]:
        
        if clear:
            self._plugins = []

        plugins_id = self.list_plugins_id()
        total = len(plugins_id)
        loaded = 0

        for id in plugins_id:
            if self.load_plugin(id):
                loaded += 1

        return (loaded, total)

    def add_plugin(self, impfrom: str, options: Optional[str | dict] = None, enable = True) -> Optional[CMagPlugin]:

        plugin = CMagPluginManagerImpl.import_plugin(impfrom)
        if not plugin:
            self.log.error(f"failed to import plugin: {impfrom}")
            return None

        if plugin.callname == '':
            self.log.error(f"plugin doesn't have callname.")
            return None

        record = self.create_plugin_record(
            callname = plugin.callname,
            impfrom = impfrom,
            options = plugin.options.to_json(),
            enable = enable
        )

        if not record:
            self.log.critical(f"something wrong with database.")
            return None

        if options != None:
            if type(options) == dict:
                options = json.dumps(options)
            self.set_plugin_options(record.id, options)

        if not enable:
            self.log.warn("plugin is not enabled.")
            return None

        return self.load_plugin(record.id)

    def remove_plugin(self):
        raise NotImplementedError

    def list_plugins(self, fields: Tuple = ()) -> List[CMagPluginModel]:
        return self.select_plugin_records(*fields)

    def list_plugins_dict(self, fields: Tuple = ()) -> List[Dict]:
        return [model_to_dict(plugin) for plugin in self.list_plugins(fields)]

    def list_plugins_id(self) -> List[int]:
        return [plugin.id for plugin in self.list_plugins((CMagPluginModel.id,))]

    def list_plugins_callname(self) -> List[str]:
        return [plugin.callname for plugin in self.list_plugins((CMagPluginModel.callname,))]

    def enable_plugin(self, id: int) -> bool:
        if not (record := self.check_plugin_record_exists_by_id(id)):
            self.log.error(f"plugin record not found: {id}")
            return False
        record.update(enable=True).execute()
        return True

    def disable_plugin(self, id: int) -> bool:
        if not (record := self.check_plugin_record_exists_by_id(id)):
            self.log.error(f"plugin record not found: {id}")
            return False
        record.update(enable=False).execute()
        return True

    def get_plugin_options(self, id: int) -> Optional[str]:
        if not (record := self.check_plugin_record_exists_by_id(id)):
            self.log.error(f"plugin record not found: {id}")
            return None
        return record.options

    def set_plugin_options(self, id: int, options: str) -> bool:
        if not (record := self.check_plugin_record_exists_by_id(id)):
            self.log.error(f"plugin record not found: {id}")
            return False
        record.update(options=options).execute()
        return True

    def load_plugin(self, id: int) -> Optional[CMagPlugin]:

        if not (record := self.check_plugin_record_exists_by_id(id)):
            self.log.error(f"plugin record not found: {id}")
            return None

        if (plugin := self.get_loaded_plugin(record.id)):
            return plugin
        
        if not record.enabled:
            self.log.warn(f"plugin not enabled: {id}")
            return None

        if not (plugin_class := CMagPluginManagerImpl.import_plugin(record.impfrom)):
            self.log.error(f"failed to import plugin: {record.impfrom}")
            return None

        plugin = plugin_class(self.project, options=record.options)
        self.plugins.append(plugin)
        return plugin

    def get_loaded_plugin(self, id: int) -> Optional[CMagPlugin]:
        for plugin in self.plugins:
            if plugin.id == id:
                return plugin

    def get_loaded_plugin_by_callname(self, callname: str) -> Optional[CMagPlugin]:
        for plugin in self.plugins:
            if plugin.callname == callname:
                return plugin

    def list_loaded_plugins(self) -> List[CMagPlugin]:
        return self.plugins

    def load_plugin_once(self, impfrom: str, options: dict = {}) -> Optional[CMagPlugin]:

        if not (plugin_class := CMagPluginManagerImpl.import_plugin(impfrom)):
            self.log.error(f"failed to import plugin: {impfrom}")
            return None

        plugin = plugin_class(self.project, options=options)
        self.plugins.append(plugin)
        return plugin

    def unload_plugin_once(self, callname: str) -> bool:
        if not (plugin := self.get_loaded_plugin_by_callname(callname)):
            self.log.error(f"failed to find plugin: {callname}")
            return False
        self.plugins.remove(plugin)
        return True
