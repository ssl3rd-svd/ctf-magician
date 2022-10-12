from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    from typing import Any, Dict, List, Optional
    from logging import Logger
    from cmag.project import CMagProject
    from cmag.challenge import CMagChallenge

import peewee
from pathlib import Path
from cmag.file.model import CMagFileModel

class CMagFileManagerImpl:
    
    TYPE_FILE = 0
    TYPE_DIR  = 1

    def __init__(self, project: CMagProject, challenge: CMagChallenge):
        self._project = project
        self._challenge = challenge
        self.path.mkdir(parents=True, exist_ok=True)
        with self.project.db as database:
            CMagFileModel.create_table()

    # properties

    @property
    def project(self) -> CMagProject:
        return self._project

    @property
    def challenge(self) -> CMagChallenge:
        return self._challenge

    @property
    def log(self) -> Logger:
        return self.challenge.log

    # database queries

    def create_file_record(self, **query) -> CMagFileModel:
        with self.project.db as database:
            return CMagFileModel.create(**query)

    def get_file_record(self, *query, **filters) -> CMagFileModel:
        with self.project.db as database:
            return CMagFileModel.get(*query, **filters)

    def get_file_record_by_id(self, id: int) -> CMagFileModel:
        with self.project.db as database:
            return CMagFileModel.get_by_id(id)

    def select_file_records(self, *fields) -> peewee.ModelSelect:
        with self.project.db as database:
            return CMagFileModel.select(*fields)

    # checker methods

    def check_file_record_exists(self, *query, **filters) -> Optional[CMagFileModel]:
        try:
            return self.get_file_record(*query, **filters)
        except peewee.DoesNotExist:
            return None

    def check_file_record_exists_by_id(self, id: int) -> Optional[CMagFileModel]:
        try:
            return self.get_file_record_by_id(id)
        except peewee.DoesNotExist:
            return None

    # path methods

    @property
    def path(self) -> Path:
        return self.project.path / 'files' / str(self.challenge.id)

    def relpath(self, dstpath: str | Path) -> Optional[Path]:

        destpath = Path(dstpath)

        if destpath.is_absolute():
            if not destpath.is_relative_to(self.path):
                return None
            else:
                destpath = destpath.relative_to(self.path)

        return destpath

    def abspath(self, dstpath: str | Path) -> Path:
        destpath = Path(dstpath)
        if not destpath.is_absolute():
            return self.path / destpath
        else:
            return destpath
