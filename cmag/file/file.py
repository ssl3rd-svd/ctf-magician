from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    from typing import Any, Dict, List, Optional
    from cmag.project import CMagProject
    from cmag.challenge import CMagChallenge
    from cmag.file.manager import CMagFileManager

from pathlib import Path
from cmag.file.model import CMagFileModel

class CMagFile:

    def __init__(self, project: CMagProject, challenge: CMagChallenge, id: int):
        self._project = project
        self._challenge = challenge
        self._manager = self.challenge.file_manager
        self._id = id

    def __repr__(self) -> str:
        return f"<CMagFile id={self.id} path=\"{self.path}\">"

    @property
    def project(self) -> CMagProject:
        return self._project

    @property
    def challenge(self) -> CMagChallenge:
        return self._challenge

    @property
    def manager(self) -> CMagFileManager:
        return self._manager

    @property
    def id(self) -> int:
        return self._id

    @property
    def record(self) -> CMagFileModel:
        return self.manager.get_file_record_by_id(self.id)

    @property
    def path(self) -> str:
        return self.record.path

    @property
    def abspath(self) -> str:
        return str(self.challenge.file_manager.path / self.path)
