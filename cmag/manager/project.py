from json import load, dump
from typing import Any, Dict, List
from pathlib import Path

from cmag.modules.Loader import CMagModuleLoader

from .Challenge import CMagChallenge, CMagChallengeImpl

from .ProjectDatabase import (
    CMagProjectDatabase,
    SqliteDatabase,
    CMagProjDatabaseProxy,
    CMagProjChallenge,
    CMagProjFile
)

class CMagProjectImpl:
    
    def __init__(self, project_root: Path, *args, **kwargs):
        
        self._dir = project_root
        self._scan_queries = {}
        
        # check structures
        for dirpath in [self.dir, self.files_dir]:
            if not dirpath.is_dir():
                raise FileNotFoundError(f"{dirpath} not found.")
        for filepath in [self.db_path, self.cfg_path]:
            if not filepath.is_file():
                raise FileNotFoundError(f"{dirpath} not found.")

        # get config
        if 'config' not in kwargs:
            with self.cfg_path.open('r') as file:
                config = load(file)
        else:
            config = kwargs['config']

        self._config = config

        # load modules
        if 'modules' in config:
            self._mods = CMagModuleLoader(self, config['modules'])
        else:
            self._mods = None

        # init logger
        if 'logger' in kwargs:
            pass # TODO

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
    def challenges(self) -> Dict[str, CMagChallengeImpl]:
        with self.database as db:
            return {c.id:CMagChallenge.load(self, c.id) for c in db.Challenge.select()}

    @property
    def mods(self): return self._mods

    # challenge operations

    def add_challenge(self):
        pass

    def upd_challenge(self):
        pass

    def del_challenge(self):
        pass

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
        
        # paths
        project_root  = project_directory
        database_file = project_directory / 'project.sqlite3'
        config_file   = project_directory / 'config.json'
        files_dir     = project_directory / 'files'

        # root dir check & initialize
        if project_root.is_dir():
            raise FileExistsError(f"{project_root} exists.")
        else:
            project_root.mkdir()
            files_dir.mkdir()

        # database initialize
        # database = SqliteDatabase(database_file)
        # CMagProjDatabaseProxy.initialize(database)
        # CMagProjChallenge.create_table()
        # CMagProjFile.create_table()
        # database.close()

        with CMagProjectDatabase(database_file) as db:
            db.Challenge.create_table()
            db.File.create_table()

        # config save
        with open(config_file, 'w') as file:
            dump(config, file)

        # load project
        return CMagProject.load(project_root,
                                config=config,
                                logger=logger)

    def load(project_root: Path, *args, **kwargs):
        return CMagProjectImpl(project_root, *args, **kwargs)

    def check():
        pass # TODO