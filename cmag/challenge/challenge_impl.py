from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    from typing import Any, Dict, List, Optional
    from cmag.project import CMagProject
    from cmag.file import CMagFile

from cmag.file.manager import CMagFileManager

from .model import CMagChallengeModel

class CMagChallengeImpl:

    def __init__(self, project: CMagProject, id: int):
        
        self._project = project
        self._id = id

        self._filemgr = CMagFileManager(self.project, self)

    @property
    def project(self) -> CMagProject:
        return self._project

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self.get_record().name

    @property
    def description(self) -> str:
        return self.get_record().name

    @property
    def file_manager(self) -> CMagFileManager:
        return self._filemgr

    def get_record(self):
        return CMagChallengeModel.get(CMagChallengeModel.id == self.id)

    def create_directory(self, *args, **kwargs) -> Optional[CMagFile]:
        return self.file_manager.create_directory(*args, **kwargs)

    def add_directory(self, *args, **kwargs) -> Optional[CMagFile]:
        return self.file_manager.add_directory(*args, **kwargs)

    def create_file(self, *args, **kwargs) -> Optional[CMagFile]:
        return self.file_manager.create_file(*args, **kwargs)

    def add_file(self, *args, **kwargs) -> Optional[CMagFile]:
        return self.file_manager.add_file(*args, **kwargs)

    def get_file_by_id(self, *args, **kwargs):
        return self.file_manager.get_file_by_id(*args, **kwargs)

    def get_file_by_path(self, *args, **kwargs):
        return self.file_manager.get_file_by_path(*args, **kwargs)

    def list_files(self, *args, **kwargs):
        return self.file_manager.list_files(*args, **kwargs)

    def remove_file(self, *args, **kwargs):
        return self.file_manager.remove_file(*args, **kwargs)