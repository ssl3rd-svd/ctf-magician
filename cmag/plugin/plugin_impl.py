from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    from typing import Any, Dict, List, Optional
    from logging import Logger
    from cmag.project import CMagProject
    from cmag.plugin.manager import CMagPluginManager

from .model import CMagPluginModel
from .option import CMagPluginOptions

class CMagPluginImpl:

    callname = ''
    start    = None
    optdef   = CMagPluginOptions

    def __init__(self, project: CMagProject):
        
        self._project = project
        self._log = project.logger.create_logger(f"plugin.{self.callname}")
        self._options = None

        if (record := self.manager.check_plugin_record_exists(CMagPluginModel.callname == self.callname)):
            self._id = record.id
        else:
            self.log.debug(f"loading plugin once: {self.callname}")
            self._id = -1

        if not self.start:
            self.start = self.run
    
    @property
    def project(self) -> CMagProject:
        return self._project

    @property
    def manager(self) -> CMagPluginManager:
        return self.project.plugin_manager

    @property
    def log(self) -> Logger:
        return self._log

    @property
    def options(self) -> Optional[CMagPluginOptions]:
        return self._options

    @property
    def id(self) -> int:
        return self._id

    @property
    def record(self) -> Optional[CMagPluginModel]:
        return self.manager.check_plugin_record_exists_by_id(self.id)

    def is_loaded_once(self) -> bool:
        return self.id == -1

    def load_options(self) -> Optional[CMagPluginOptions]:

        if not (record := self.record):
            self.log.debug(f"there are no record save to: {self.callname}")
            return False

        return self.load_options_from_json(record.options)

    def load_default_options(self) -> CMagPluginOptions:
        return self.load_options_from_dict({})

    def load_options_from_dict(self, options: dict) -> Optional[CMagPluginOptions]:
        if (options := self.optdef.from_dict(options)):
            self._options = options
            return options

    def load_options_from_json(self, options: str) -> Optional[CMagPluginOptions]:
        if (options := self.optdef.from_json(options)):
            self._options = options
            return options

    def save_options_to_db(self) -> bool:

        if not (options := self.options):
            self.log.debug(f"there are no options to save: {self.callname}")
            return False

        if not (record := self.record):
            self.log.debug(f"there are no record save to: {self.callname}")
            return False

        record.update(options=options.to_json())
        return True

    def run(self, *args, **kwargs):
        raise NotImplementedError
