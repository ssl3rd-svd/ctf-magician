from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    from typing import Any, Dict, List

from pathlib import Path

from cmag.database import CMagDatabase
from cmag.challenge import CMagChallenge
from cmag.challenge.manager import CMagChallengeManager
from cmag.plugin.manager import CMagPluginManager

class CMagProjectImpl:

    def __init__(self, project_dir:str):
        
        self._dir = project_dir
        self.path.mkdir(exist_ok=True)

        self._challmgr = CMagChallengeManager(self)
        self._plginmgr = CMagPluginManager(self)

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
        return self.challenge_manager.remove_challenge(*args, **kwargs)

    def add_plugin(self, *args, **kwargs):
        return self.plugin_manager.add_plugin(*args, **kwargs)

    def enable_plugin(self, *args, **kwargs):
        return self.plugin_manager.enable_plugin(*args, **kwargs)

    def disable_plugin(self, *args, **kwargs):
        return self.plugin_manager.disable_plugin(*args, **kwargs)

    def load_all(self, *args, **kwargs):
        return self.plugin_manager.load_all(*args, **kwargs)

    def load_plugin_once(self, *args, **kwargs):
        return self.plugin_manager.load_plugin_once(*args, **kwargs)

    def load_plugin(self, *args, **kwargs):
        return self.plugin_manager.load_plugin(*args, **kwargs)

    def get_loaded_plugin(self, *args, **kwargs):
        return self.plugin_manager.get_loaded_plugin(*args, **kwargs)

    def list_plugins(self, *args, **kwargs):
        return self.plugin_manager.list_plugins(*args, **kwargs)

    def list_loaded_plugins(self, *args, **kwargs):
        return self.plugin_manager.list_loaded_plugins(*args, **kwargs)

    def save_loaded_plugin_options(self, *args, **kwargs):
        return self.plugin_manager.save_loaded_plugin_options(*args, **kwargs)

    def unload_plugin_once(self, *args, **kwargs):
        return self.plugin_manager.unload_plugin_once(*args, **kwargs)

    def unload_plugin(self, *args, **kwargs):
        return self.plugin_manager.unload_plugin(*args, **kwargs)
