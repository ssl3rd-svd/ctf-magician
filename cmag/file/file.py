from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    from typing import Any, Dict, List, Optional
    from cmag.project import CMagProject
    from cmag.challenge import CMagChallenge

from cmag.file.model import CMagFileModel

class CMagFile:

    def __init__(self, project: CMagProject, challenge: CMagChallenge, id: int):
        self._project = project
        self._challenge = challenge
        self._id = id

    @property
    def project(self) -> CMagProject:
        return self._project

    @property
    def challenge(self) -> CMagChallenge:
        return self._challenge

    @property
    def id(self) -> int:
        return self._id

    @property
    def path(self) -> str:
        return self.get_record().path

    def get_record(self) -> CMagFileModel:
        return CMagFileModel.get(CMagFileModel.id == self.id)
