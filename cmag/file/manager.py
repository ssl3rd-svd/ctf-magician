from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    from typing import Any, Dict, List, Optional

from pathlib import Path
from shutil import copyfile
from cmag.file import CMagFile
from cmag.file.model import CMagFileModel
from cmag.file.manager_impl import CMagFileManagerImpl

class CMagFileManager(CMagFileManagerImpl):

    def __repr__(self) -> str:
        return f"<CMagFileManager files={len(self.list_files())}>"

    def create_file(self, dstpath: str) -> Optional[CMagFile]:

        dstpath = self.relpath(dstpath)
        if not dstpath:
            self.log.error(f"wrong path passed: {dstpath}")
            return None

        self.abspath(dstpath).touch()

        self.log.debug(f"file {dstpath} created.")

        record = self.create_file_record(
            root=0,
            type=CMagFileManager.TYPE_FILE,
            path=dstpath,
            challenge=self.challenge.record
        )

        if not record:
            self.log.critical(f"unknown error occured while creating file record.")
            return None

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

        self.log.debug(f"file {source} copied to {absdest}")

        record = self.create_file_record(
            root=0,
            type=CMagFileManager.TYPE_FILE,
            path=dest,
            challenge=self.challenge.record
        )

        if not record:
            self.log.critical(f"unknown error occured while creating file record.")
            return None

        return CMagFile(self.project, self.challenge, record.id)

    def get_file(self, id: int) -> Optional[CMagFile]:

        if not (record := self.check_file_record_exists_by_id(id)):
            self.log.error(f"there are no file record: {id}")
            return None

        return CMagFile(self.project, self.challenge, record.id)

    def get_file_by_path(self, path: str) -> Optional[CMagFile]:

        if not (record := self.check_file_record_exists(CMagFileModel.path == path)):
            self.log.error(f"there are no file record: {path}")
            return None

        return CMagFile(self.project, self.challenge, record.id)

    def list_files(self) -> List[CMagFile]:
        return [CMagFile(self.project, self.challenge, record.id) for record in self.select_file_records()]

    def remove_file(self):
        raise NotImplementedError