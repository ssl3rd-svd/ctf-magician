from __future__ import annotations
import typing

if typing.TYPE_CHECKING:
    from typing import Any, Dict, List, Optional
    from logging import Logger
    from cmag.project import CMagProject
    from cmag.challenge.manager import CMagChallengeManager

from cmag.file.manager import CMagFileManager
from cmag.challenge.model import CMagChallengeModel

class CMagChallengeImpl:

    def __init__(self, project: CMagProject, id: int):
        self._id = id
        self._project = project
        self._log = project.logger.create_logger(f"challenge.{id}")
        self._filemgr = CMagFileManager(self.project, self)

    @property
    def id(self) -> int:
        return self._id

    @property
    def project(self) -> CMagProject:
        return self._project

    @property
    def manager(self) -> CMagChallengeManager:
        return self.project.challenge_manager

    @property
    def log(self) -> Logger:
        return self._log

    @property
    def file_manager(self) -> CMagFileManager:
        return self._filemgr

    @property
    def record(self) -> CMagChallengeModel:
        return self.manager.get_challenge_record_by_id(self.id)
