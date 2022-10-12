from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    from typing import Any, Dict, List, Optional

from cmag.challenge.challenge_impl import CMagChallengeImpl

class CMagChallenge(CMagChallengeImpl):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __repr__(self) -> str:
        return f"<CMagChallenge id={self.id} name=\"{self.name}\">"

    @property
    def name(self) -> str:
        return self.record.name

    @property
    def description(self) -> str:
        return self.record.name

    def create_file(self, *args, **kwargs):
        return self.file_manager.create_file(*args, **kwargs)

    def add_file(self, *args, **kwargs):
        return self.file_manager.add_file(*args, **kwargs)

    def get_file(self, *args, **kwargs):
        return self.file_manager.get_file(*args, **kwargs)

    def get_file_by_path(self, *args, **kwargs):
        return self.file_manager.get_file_by_path(*args, **kwargs)

    def list_files(self, *args, **kwargs):
        return self.file_manager.list_files(*args, **kwargs)

    def remove_file(self, *args, **kwargs):
        return self.file_manager.remove_file(*args, **kwargs)