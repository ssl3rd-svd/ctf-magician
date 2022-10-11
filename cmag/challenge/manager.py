from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    from typing import Any, Dict, List, Optional
    from cmag.project import CMagProject

from .challenge import CMagChallenge
from .model import CMagChallengeModel

class CMagChallengeManager:

    def __init__(self, project: CMagProject):

        self._project = project

        with self.project.db as database:
            CMagChallengeModel.create_table()

    @property
    def project(self) -> CMagProject:
        return self._project

    def add_challenge(self, name: str) -> Optional[CMagChallenge]:
        with self.project.db as database:
            record = CMagChallengeModel.create(name=name)
            if record:
                return CMagChallenge(self.project, record.id)

    def get_challenge_by_id(self, id: int) -> Optional[CMagChallenge]:
        with self.project.db as database:
            record = CMagChallengeModel.get(id=id)
            if record:
                return CMagChallenge(self.project, record.id)

    def get_challenge_by_name(self, name: str) -> Optional[CMagChallenge]:
        with self.project.db as database:
            record = CMagChallengeModel.get(name=name)
            if record:
                return CMagChallenge(self.project, record.id)

    def list_challenges(self) -> Dict[int, str]:
        with self.project.db as database:
            records = CMagChallengeModel.select()
            if records:
                return {record.id:record.name for record in records}
        return {}

    def remove_challenge(self, id: int) -> int:
        with self.project.db as database:
            record = CMagChallengeModel.get(id=id)
            if record:
                return record.delete_instance()