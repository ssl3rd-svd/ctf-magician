from __future__ import annotations
import typing

from cmag.challenge.exceptions import CMagChallMgrImplSelectError

if typing.TYPE_CHECKING:
    from typing import Any, Dict, List, Optional
    from logging import Logger
    from cmag.project import CMagProject
    from cmag.interface.logger import CMagLogger

import peewee
from cmag.challenge.model import CMagChallengeModel
from .exceptions import Exception, CMagChallMgrImplInitError, CMagChallMgrImplCreateError, CMagChallMgrImplGetError, CMagChallMgrImplGetByIdError, CMagChallMgrImplSelectError

class CMagChallengeManagerImpl:

    @Exception(CMagChallMgrImplInitError)
    def __init__(self, project: CMagProject):
        self._project = project
        self._log = project.logger.create_logger('challenge_manager')
        with self.project.db as database:
            CMagChallengeModel.create_table()

    # properties

    @property
    def project(self) -> CMagProject:
        return self._project

    @property
    def log(self) -> Logger:
        return self._log

    # database queries

    @Exception(CMagChallMgrImplCreateError)
    def create_challenge_record(self, **query) -> CMagChallengeModel:
        with self.project.db as database:
            return CMagChallengeModel.create(**query)

    @Exception(CMagChallMgrImplGetError)
    def get_challenge_record(self, *query, **filters) -> CMagChallengeModel:
        with self.project.db as database:
            return CMagChallengeModel.get(*query, **filters)

    @Exception(CMagChallMgrImplGetByIdError)
    def get_challenge_record_by_id(self, id: int) -> CMagChallengeModel:
        with self.project.db as database:
            return CMagChallengeModel.get_by_id(id)

    @Exception(CMagChallMgrImplSelectError)
    def select_challenge_records(self, *fields) -> peewee.ModelSelect:
        with self.project.db as database:
            return CMagChallengeModel.select(*fields)

    # checkers

    def check_challenge_record_exists(self, *query, **filters) -> Optional[CMagChallengeModel]:
        try:
            return self.get_challenge_record(*query, **filters)
        except peewee.DoesNotExist:
            return None

    def check_challenge_record_exists_by_id(self, id: int) -> Optional[CMagChallengeModel]:
        try:
            return self.get_challenge_record_by_id(id)
        except peewee.DoesNotExist:
            return None