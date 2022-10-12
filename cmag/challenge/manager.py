from __future__ import annotations
import typing

if typing.TYPE_CHECKING:
    from typing import Any, Dict, List, Optional

from cmag.challenge.manager_impl import CMagChallengeManagerImpl
from cmag.challenge.model import CMagChallengeModel
from cmag.challenge.challenge import CMagChallenge

class CMagChallengeManager(CMagChallengeManagerImpl):

    def __repr__(self) -> str:
        return f"<CMagChallengeManager challenges={len(self.list_challenges())}>"

    def add_challenge(self, name: str) -> Optional[CMagChallenge]:

        if not (record := self.create_challenge_record(name=name)):
            self.log.error(f"failed to create challenge record: {name}")
            return None

        return CMagChallenge(self.project, record.id)

    def get_challenge(self, id: int) -> Optional[CMagChallenge]:

        if not (record := self.check_challenge_record_exists_by_id(id)):
            self.log.error(f"failed to get challenge record: {id}")
            return None

        return CMagChallenge(self.project, record.id)

    def get_challenge_by_name(self, name: str) -> Optional[CMagChallenge]:

        if not (record := self.check_challenge_record_exists(CMagChallengeModel.name == name)):
            self.log.error(f"failed to get challenge record: {name}")
            return None

        return CMagChallenge(self.project, record.id)

    def list_challenges(self) -> List[CMagChallenge]:
        return [CMagChallenge(self.project, record.id) for record in self.select_challenge_records()]

    def remove_challenge(self, id: int) -> int:
        
        if not (record := self.check_challenge_record_exists_by_id(id)):
            self.log.error(f"failed to get challenge record: {id}")
            return None

        record.delete_instance()
