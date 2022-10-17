from __future__ import annotations
import typing

from cmag.challenge.exceptions import CMagChallFailed, CMagChallImplFailed, CMagChallMgrImplFailed, CMagChallModelFailed

if typing.TYPE_CHECKING:
    from typing import Any, Dict, List, Optional
    from cmag.project import CMagProject

import peewee
from cmag.challenge.manager_impl import CMagChallengeManagerImpl
from cmag.challenge.model import CMagChallengeModel
from cmag.challenge.challenge import CMagChallenge
from .exceptions import CMagChallMgrFailed, handle_except_decorate

class CMagChallengeManager(CMagChallengeManagerImpl):

    def __repr__(self) -> str:
        return f"<CMagChallengeManager challenges={len(self.list_challenges())}>"

    def handle_exception(self, e):
        # TODO: handle exception at challenge layer
        error = e.__class__
        if issubclass(error, peewee.IntegrityError):
            self.log.error(f"challenge file already exists.")
            raise CMagChallMgrFailed
        elif issubclass(error, CMagChallMgrImplFailed):
            self.log.error(e)
            raise CMagChallMgrFailed
        elif issubclass(error, CMagChallFailed):
            self.log.error(e)
            raise CMagChallMgrFailed
        elif issubclass(error, CMagChallImplFailed):
            self.log.error(e)
            raise CMagChallMgrFailed
        elif issubclass(error, CMagChallModelFailed):
            self.log.error(e)
            raise CMagChallMgrFailed

    @handle_except_decorate(handle_exception)
    def add_challenge(self, name: str) -> Optional[CMagChallenge]:

        if not (record := self.create_challenge_record(name=name)):
            self.log.error(f"failed to create challenge record: {name}")
            return None

        return CMagChallenge(self.project, record.id)

    @handle_except_decorate(handle_exception)
    def get_challenge(self, id: int) -> Optional[CMagChallenge]:

        if not (record := self.check_challenge_record_exists_by_id(id)):
            self.log.error(f"failed to get challenge record: {id}")
            return None

        return CMagChallenge(self.project, record.id)

    @handle_except_decorate(handle_exception)
    def get_challenge_by_name(self, name: str) -> Optional[CMagChallenge]:

        if not (record := self.check_challenge_record_exists(CMagChallengeModel.name == name)):
            self.log.error(f"failed to get challenge record: {name}")
            return None

        return CMagChallenge(self.project, record.id)

    @handle_except_decorate(handle_exception)
    def list_challenges(self) -> List[CMagChallenge]:
        return [CMagChallenge(self.project, record.id) for record in self.select_challenge_records()]

    @handle_except_decorate(handle_exception)
    def remove_challenge(self, id: int) -> bool:
        
        if not (record := self.check_challenge_record_exists_by_id(id)):
            self.log.error(f"failed to get challenge record: {id}")
            return False

        record.delete_instance()
        return True