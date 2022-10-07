from __future__ import annotations

if __import__("typing").TYPE_CHECKING:
    from typing import Any, Dict, List

import json
from pathlib import Path
from cmag.project.database import CMagProjectDatabase
from .ProjectConfig import CMagProjectConfig
from .ProjectImpl import CMagProjectImpl

class CMagProject(CMagProjectImpl):

    def create(project_directory: str | Path,
               cfg_load_file: str | Path = '',
               cfg_load_data: Dict[str, Any] = {},
               logger: Any = None,
               *args, **kwargs) -> CMagProject:
        
        project_directory = Path(project_directory)

        if (project_root := project_directory).is_dir():
            raise Exception
        else:
            project_root.mkdir()
            (files_dir := project_root / 'files').mkdir()
            (plugins_dir := project_directory / 'plugins').mkdir()

        database_file = project_directory / 'project.sqlite3'
        with CMagProjectDatabase(database_file) as db:
            db.Challenge.create_table()
            db.File.create_table()

        config_file = project_directory / 'config.json'
        CMagProjectConfig(config_file).savefile()

        project = CMagProject(project_directory,
                              cfg_load_file=cfg_load_file,
                              cfg_load_data=cfg_load_data,
                              *args, **kwargs)
        return project
        
    def load(project_directory: str | Path,
             cfg_load_file: str | Path = '',
             cfg_load_data: Dict[str, Any] = {},
             cfg_load_default: bool = False,
             *args, **kwargs) -> CMagProject:

        return CMagProject(project_directory,
                           cfg_load_file=cfg_load_file,
                           cfg_load_data=cfg_load_data,
                           *args, **kwargs)

    def check(project_directory: str | Path) -> bool:
        ...

    def scan_challenge(self, chall_id: str):

        if chall_id not in self._scan_queries:
            self._scan_queries[chall_id] = []

        if not self._scan_queries[chall_id]:
            for plugin in self.plugins.initial_scanners:
                self.scan_query(chall_id, plugin.run, chall_id)

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