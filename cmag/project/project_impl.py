from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    from typing import Any, Dict, List

from pathlib import Path

from cmag.database import CMagDatabase
from cmag.challenge import CMagChallenge
from cmag.challenge.manager import CMagChallengeManager

class CMagProjectImpl:

    def __init__(self, project_dir:str):
        
        self._dir = project_dir
        self.path.mkdir(exist_ok=True)

        self._challmgr = CMagChallengeManager(self)
        self._plginmgr = None

    @property
    def dir(self):
        return self._dir

    @property
    def path(self):
        return Path(self.dir)

    @property
    def db(self):
        return CMagDatabase(self.path / 'project.db')

    @property
    def challenge_manager(self):
        return self._challmgr

    @property
    def plugin_manager(self):
        return self._plginmgr

    def add_challenge(self, *args, **kwargs) -> CMagChallenge:
        return self.challenge_manager.add_challenge(*args, **kwargs)

    def get_challenge_by_id(self, *args, **kwargs) -> CMagChallenge:
        return self.challenge_manager.get_challenge_by_id(*args, **kwargs)

    def get_challenge_by_name(self, *args, **kwargs) -> CMagChallenge:
        return self.challenge_manager.get_challenge_by_name(*args, **kwargs)

    def list_challenges(self, *args, **kwargs) -> Dict[int, str]:
        return self.challenge_manager.list_challenges(*args, **kwargs)

    def remove_challenge(self, *args, **kwargs):
        self.challenge_manager.remove_challenge(*args, **kwargs)

    def add_plugin(self):
        pass

    def remove_plugin(self):
        pass

    def load_plugin(self):
        pass

    def unload_plugin(self):
        pass
