from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    from typing import Any, Dict, List, Optional
    from cmag.project import CMagProject
    from cmag.challenge import CMagChallenge
import os
from pathlib import Path
from shutil import copyfile
from cmag.file import CMagFile
from cmag.file.model import CMagFileModel

class CMagFileManager:
    
    TYPE_FILE = 0
    TYPE_DIR  = 1

    def __init__(self, project: CMagProject, challenge: CMagChallenge):
        self._project = project
        self._challenge = challenge
        self.path.mkdir(parents=True, exist_ok=True)
        with self.project.db as database:
            CMagFileModel.create_table()

    @property
    def project(self) -> CMagProject:
        return self._project

    @property
    def challenge(self) -> CMagChallenge:
        return self._challenge

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
        if not dstpath.is_absolute():
            return self.path / dstpath
        else:
            return dstpath

    def create_directory(self, dstpath: str):
        try:
            if not os.path.exists(self.abspath(dstpath)):
                os.makedirs(self.abspath(dstpath))
        except OSError:
            raise Exception('creating file directory error')

    def add_directory(self, srcpath: str, dstpath: str):
        raise NotImplementedError

    def create_file(self, dstpath: str) -> Optional[CMagFile]:

        dstpath = self.relpath(dstpath)
        if not dstpath:
            return None

        self.abspath(dstpath).touch()

        with self.project.db as database:
            record = CMagFileModel.create(
                root=0, 
                type=CMagFileManager.TYPE_FILE, 
                path=dstpath, 
                challenge=self.challenge.get_record()
            )
            if record:
                return CMagFile(self.project, self.challenge, record.id)

    def add_file(self, srcpath: str, dstpath: str = '') -> Optional[CMagFile]:

        source = Path(srcpath)

        if dstpath:
            dest = self.relpath(dstpath)
            if not dest:
                return None
        else:
            dest = source.name

        absdest = self.abspath(dest)
        copyfile(source, absdest)

        with self.project.db as database:
            record = CMagFileModel.create(
                root=0,
                type=CMagFileManager.TYPE_FILE, 
                path=dest, 
                challenge=self.challenge.get_record()
            )
            if record:
                return CMagFile(self.project, self.challenge, record.id)

    def get_file_by_id(self, id: int) -> Optional[CMagFile]:
        with self.project.db as database:
            record = CMagFileModel.get(CMagFileModel.id == id)
            if record:
                return CMagFile(self.project, self.challenge, record.id)

    def get_file_by_path(self, path: str) -> Optional[CMagFile]:
        with self.project.db as database:
            record = CMagFileModel.get(CMagFileModel.path == path)
            if record:
                return CMagFile(self.project, self.challenge, record.id)

    def list_files(self) -> Dict[int:str]:
        with self.project.db as database:
            records = self.challenge.get_record().files
            if records:
                return {record.id:record.path for record in records}
        return {}

    def remove_file(self):
        raise NotImplementedError