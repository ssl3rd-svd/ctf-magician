from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    from typing import Any, Dict, List, Optional
    from cmag.project import CMagProject

from .model import CMagPluginModel
from .option import CMagPluginOptions

class CMagPlugin:

    callname = ''
    start = None
    optdef = CMagPluginOptions

    def __init__(self, project: CMagProject, id: int, options: str | Dict = {}):
        
        self._project = project
        self._id = id
        self._options = None

        if type(options) == str and options != '':
            self.load_json_options(options)
        elif type(options) == dict and options != {}:
            self.load_options(options)
        
        if self._options == None:
            self.load_options_from_db()
        if self._options == None:
            self.load_default_options()
        
        if not self.start:
            self.start = self.run
    
    @property
    def project(self):
        return self._project

    @property
    def id(self):
        return self._id

    @property
    def options(self):
        return self._options

    def is_loaded_once(self):
        return self.id == -1

    def get_record(self):
        if self.is_loaded_once:
            return None
        with self.project.db as database:
            return CMagPluginModel.get(CMagPluginModel.id == self.id)

    def load_options(self, options: dict):
        self._options = self.optdef.from_dict(options)
        return self._options

    def load_json_options(self, options: str):
        self._options = self.optdef.from_json(options)
        return self._options

    def load_default_options(self):
        return self.load_options({})

    def load_options_from_db(self):
        if (record := self.get_record()) and record.options:
            self._options = self.optdef.from_json(record.options)
        return self._options

    def save_options_to_db(self):
        if self._options:
            options = self._options.to_json()
            record = self.get_record()
            if record:
                record.update(options=options)

    def run(self, *args, **kwargs):
        raise NotImplementedError