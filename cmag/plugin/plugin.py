from __future__ import annotations
import typing

if typing.TYPE_CHECKING:
    from typing import Dict
    from cmag.project.project import CMagProject

from .plugin_impl import CMagPluginImpl

class CMagPlugin(CMagPluginImpl):

    def __init__(self, project: CMagProject, options: str | Dict = {}):

        super().__init__(project)

        if type(options) == str and options != '':
            self.load_options_from_json(options)
        elif type(options) == dict and options != {}:
            self.load_options_from_dict(options)
        
        if self._options == None:
            self.load_options() # from db.
        if self._options == None:
            self.load_default_options()

    def __repr__(self) -> str:
        return f"<{type(self).__name__} id={self.id}, callname=\"{self.callname}\">"
