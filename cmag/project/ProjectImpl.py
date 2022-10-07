from __future__ import annotations

if __import__("typing").TYPE_CHECKING:
    from typing import Any, Dict, List

from pathlib import Path

from cmag.project.challenge import CMagChallengeManager
from cmag.project.database import CMagProjectDatabase
from cmag.project.loader import CMagPluginLoader
from cmag.project.exception import *
from .ProjectConfig import CMagProjectConfig

class CMagProjectImpl:
    
    def __init__(self, project_root: str | Path,
                       cfg_load_file: str | Path = '',
                       cfg_load_data: Dict[str, Any] = {},
                       logger: Any = None,
                       *args, **kwargs):
        
        self._dir = Path(project_root)
        self._scan_queries = {}

        self._config = CMagProjectConfig(self.cfg_path)
        if cfg_load_data:
            self.config.load(cfg_load_data)
        elif cfg_load_file:
            self.config.load_from_file(cfg_load_file)

        self._plugins = CMagPluginLoader(self, self.config['plugins'], ["cmag.plugin"])
        self._challenges = CMagChallengeManager(self)

    # paths

    @property
    def dir(self): return self._dir

    @property
    def cfg_path(self): return self.dir / 'config.json'

    @property
    def db_path(self): return self.dir / 'project.sqlite3'

    @property
    def files_dir(self): return self.dir / 'files'

    @property
    def plugins_dir(self): return self.dir / 'plugins'

    # components

    @property
    def config(self): return self._config

    @property
    def database(self): return CMagProjectDatabase(self.db_path)

    @property
    def plugins(self): return self._plugins

    @property
    def challenges(self): return self._challenges
