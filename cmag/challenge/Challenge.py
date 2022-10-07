from __future__ import annotations
import typing

if typing.TYPE_CHECKING:
    from typing import Any, Dict, List
    from cmag.project.Project import CMagProject

import warnings
import shutil
from .ChallengeImpl import CMagChallengeImpl as impl

class CMagChallenge(impl):
    
    # static methods --

    def new(challenge_dir: str,
            cfg_load_file: str = '',
            cfg_load_dict: Dict[str, Any] = {},
            cfg_load_default: bool = False):
        
        if not (cfg_load_file or cfg_load_dict or cfg_load_default):
            warnings.warn('config args not passed. (file, dict, default)')
            return None

        return CMagChallenge(challenge_dir,
                             cfg_load_file, cfg_load_dict,
                             cfg_load_default, True)

    def load(challenge_dir: str,
             cfg_load_file: str = '',
             cfg_load_dict: Dict[str, Any] = {},
             cfg_load_default: bool = False,
             cfg_save_on_init: bool = True):
        
        return CMagChallenge(challenge_dir,
                             cfg_load_file, cfg_load_dict,
                             cfg_load_default, cfg_save_on_init)

    def check(challenge_dir: str):
        pass
