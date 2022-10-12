from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    from typing import Any, Dict, List, Optional, Tuple
    from logging import Logger
    from cmag.project import CMagProject

import sys
import peewee

from importlib import import_module
from pathlib import Path
from cmag.plugin import CMagPlugin
from cmag.plugin.model import CMagPluginModel

class CMagPluginManagerImpl:

    def __init__(self, project: CMagProject):
        self._project = project
        self._log = project.logger.create_logger('plugin_manager')
        self._plugins = []
        with self.project.db as database:
            CMagPluginModel.create_table()

    # properties

    @property
    def project(self) -> CMagProject:
        return self._project

    @property
    def log(self) -> Logger:
        return self._log

    @property
    def plugins(self) -> List[CMagPlugin]:
        return self._plugins

    # database queries

    def create_plugin_record(self, **query) -> CMagPluginModel:
        with self.project.db as database:
            return CMagPluginModel.create(**query)

    def get_plugin_record(self, *query, **filters) -> CMagPluginModel:
        with self.project.db as database:
            return CMagPluginModel.get(*query, **filters)

    def get_plugin_record_by_id(self, id: int) -> CMagPluginModel:
        with self.project.db as database:
            return CMagPluginModel.get_by_id(id)

    def select_plugin_records(self, *fields) -> peewee.ModelSelect:
        with self.project.db as database:
            return CMagPluginModel.select(*fields)

    # checkers

    def check_plugin_record_exists(self, *query, **filters) -> Optional[CMagPluginModel]:
        try:
            return self.get_plugin_record(*query, **filters)
        except peewee.DoesNotExist:
            return None

    def check_plugin_record_exists_by_id(self, id: int) -> Optional[CMagPluginModel]:
        try:
            return self.get_plugin_record_by_id(id)
        except peewee.DoesNotExist:
            return None

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

        return CMagPluginManagerImpl.get_plugin_from_module(module)

    def import_plugin(module_name: str) -> Optional[CMagPlugin]:

        try:
            module = import_module(module_name)
        except ModuleNotFoundError:
            module = None # catch exception here, and...

        if not module:
            return CMagPluginManagerImpl.import_plugin_by_path(module_name)

        return CMagPluginManagerImpl.get_plugin_from_module(module)
