from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    from typing import Any, Dict, List
    from cmag.challenge import CMagChallenge

import shutil
import warnings
from secrets import token_hex
from .ProjectImpl import CMagProjectImpl as impl

class CMagProject(impl):

    # static methods --

    def new(project_dir: str,
            cfg_load_file: str = '',
            cfg_load_dict: Dict[str, Any] = {},
            cfg_load_default: bool = False) -> CMagProject | None:
        
        if not (cfg_load_file or cfg_load_dict or cfg_load_default):
            warnings.warn('config args not passed. (file, dict, default)')
            return None

        return CMagProject(project_dir,
                           cfg_load_file,
                           cfg_load_dict,
                           cfg_load_default,
                           True)

    def load(project_dir: str,
             cfg_load_file: str = '',
             cfg_load_dict: Dict[str, Any] = {},
             cfg_load_default: bool = False,
             cfg_save_on_init: bool = False) -> CMagProject:
        
        return CMagProject(project_dir,
                           cfg_load_file,
                           cfg_load_dict,
                           cfg_load_default,
                           cfg_save_on_init)

    def check(project_dir: str) -> bool:
        return True

    # config funcs --

    def save(self):
        self.cfg.save()
        for dirname, challenge in self.challenges.items():
            challenge.cfg.save()

    # challenge funcs --

    def load_challenges(self):
        for dirname in self.cfg['challenges']:
            self.load_challenge(dirname)
