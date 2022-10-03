from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing       import Any, Dict, List
    from cmag.manager import CMagChallengeImpl

from json                         import (load as load_json,
                                          dump as dump_json)
from pathlib                      import Path
from cmag.modules                 import CMagModuleLoader
from cmag.manager.Challenge       import CMagChallenge
from cmag.manager.ProjectDatabase import CMagProjectDatabase
from cmag.manager.exception       import CMagConfigNotFound

class CMagProjectImpl:
    
    def __init__(self, project_root: Path, *args, **kwargs):
        
        self._dir = project_root
        self._scan_queries = {}
        self._challenges = {}
        self._loading_challenges = False

        # init logger
        if 'logger' in kwargs:
            pass # TODO
        
        # check directories
        for dirpath in [self.dir, self.files_dir]:
            if not dirpath.is_dir():
                raise FileNotFoundError(f"{dirpath} not found.")

        # check files
        for filepath in [self.db_path, self.cfg_path]:
            if not filepath.is_file():
                raise FileNotFoundError(f"{dirpath} not found.")

        # get config
        if 'config' not in kwargs:
            with self.cfg_path.open('r') as file:
                config = load_json(file)
        else:
            config = kwargs['config']

        self._config = config

        # load modules
        if 'modules' not in config:
            raise CMagConfigNotFound('modules')
        else:
            self._mods = CMagModuleLoader(self, config['modules'])

    @property
    def dir(self): return self._dir

    @property
    def db_path(self): return self.dir / 'project.sqlite3'

    @property
    def cfg_path(self): return self.dir / 'config.json'

    @property
    def files_dir(self): return self.dir / 'files'

    @property
    def config(self): return self._config

    @property
    def database(self): return CMagProjectDatabase(self.db_path)

    @property
    def challenges(self) -> List[str]:
        with self.database as db:
            return [c.id for c in db.Challenge.select()]

    @property
    def mods(self): return self._mods

    # challenge operations

    def challenge(self, id):
        return CMagChallenge.load(self, id)

    def add_challenge(self):
        raise NotImplementedError

    def upd_challenge(self):
        raise NotImplementedError

    def del_challenge(self):
        raise NotImplementedError

    # scanning operations

    def scan_challenge(self, chall_id: str):

        self._scan_queries[chall_id] = []

        for mod in self.mods.initial_scanners:
            self.scan_add(chall_id, mod.run, chall_id)

        while self._scan_queries[chall_id]:
            scanner, args, kwargs = self._scan_queries[chall_id].pop(0)
            scanner(*args, **kwargs)

    def scan_add(self, chall_id: str, scanner, *args, **kwargs):
        self._scan_queries[chall_id].append((scanner, args, kwargs))

class CMagProject:

    def new(project_directory: Path,
            config: Dict[str, Any] = {},
            logger: Any = None) -> CMagProjectImpl:
        
        project_root  = project_directory
        database_file = project_directory / 'project.sqlite3'
        config_file   = project_directory / 'config.json'
        files_dir     = project_directory / 'files'

        # init directories
        project_root.mkdir()
        files_dir.mkdir()

        # create database
        with CMagProjectDatabase(database_file) as db:
            db.Challenge.create_table()
            db.File.create_table()

        # save config to file
        with open(config_file, 'w') as file:
            dump_json(config, file)

        # load project
        return CMagProject.load(project_root, config=config, logger=logger)

    def load(project_root: Path, *args, **kwargs):
        return CMagProjectImpl(project_root, *args, **kwargs)

    def check():
        raise NotImplementedError