from __future__ import annotations
if __import__("typing").TYPE_CHECKING:
    from typing import Any, Dict, List

from pathlib import Path
from cmag.project.challenge import CMagChallengeManager
from cmag.project.database import CMagProjectDatabase
from cmag.project.loader import CMagPluginLoader
from cmag.project.config import CMagConfig
from cmag.project.exception import *
from .ProjectConfig import CMagProjectConfig

class CMagProject:
    
    def __init__(self, project_root: Path, logger: Any = None, *args, **kwargs):
        
        self._dir = project_root
        self._scan_queries = {}

        self._config     = CMagProjectConfig(self.cfg_path)
        self._plugins    = CMagPluginLoader(self, self.config['plugins'], ["cmag.plugin"])
        self._challenges = CMagChallengeManager(self)

    # paths

    @property
    def dir(self): return self._dir

    @property
    def db_path(self): return self.dir / 'project.sqlite3'

    @property
    def cfg_path(self): return self.dir / 'config.json'

    @property
    def files_dir(self): return self.dir / 'files'

    # components

    @property
    def config(self): return self._config

    @property
    def database(self): return CMagProjectDatabase(self.db_path)

    @property
    def plugins(self): return self._plugins

    @property
    def challenges(self): return self._challenges

    # scanning operations

    def scan_challenge(self, chall_id: str):

        self._scan_queries[chall_id] = []

        for mod in self.mods.initial_scanners:
            self.scan_query(chall_id, mod.run, chall_id)

        while self._scan_queries[chall_id]:
            scanner, args, kwargs = self._scan_queries[chall_id].pop(0)
            scanner(*args, **kwargs)

    def scan_query(self, chall_id: str, scanner, *args, **kwargs):
        self._scan_queries[chall_id].append((scanner, args, kwargs))

    def scan_query_next(self, chall_id: str, scanner, *args, **kwargs):
        self._scan_queries[chall_id].insert(0, (scanner, args, kwargs))

    def scan_cancel_after(self, chall_id, index: int):
        self._scan_queries[chall_id] = self._scan_queries[chall_id][:index]

    def scan_cancel_all(self, chall_id: str):
        self._scan_queries[chall_id] = []