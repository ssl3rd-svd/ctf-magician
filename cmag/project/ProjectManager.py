from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing       import Any, Dict, List
    from cmag.project.challenge import CMagChallengeImpl

from pathlib import Path
from cmag.project.database import CMagProjectDatabase
from cmag.project.config import CMagConfig

from .Project import CMagProject
from .ProjectConfig import CMagProjectConfigFields as configfields

class CMagProjectManager:

    def new(project_directory: Path,
            config: Dict[str, Any] = {},
            logger: Any = None) -> CMagProject:
        
        project_directory = Path(project_directory)

        (project_root := project_directory).mkdir()
        (files_dir := project_directory / 'files').mkdir()
        database_file = project_directory / 'project.sqlite3'
        config_file = project_directory / 'config.json'

        # create database
        with CMagProjectDatabase(database_file) as db:
            db.Challenge.create_table()
            db.File.create_table()

        # save initial config to file
        cfg = CMagConfig(configfields, config_file, config)
        cfg.save()

        # load project
        return CMagProject.load(project_root, logger=logger)

    def load(project_root: Path, *args, **kwargs):
        return CMagProject(project_root, *args, **kwargs)

    def check():
        raise NotImplementedError
