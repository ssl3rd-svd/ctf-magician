from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    from typing import Any, Dict, List, Optional

from cmag.challenge.challenge_impl import CMagChallengeImpl
from .exceptions import raise_except_decorate, CMagChallListError, CMagChallInitError, CMagChallCreateError, CMagChallAddError, CMagChallGetByPathError, CMagChallGetError, CMagChallRemoveError

class CMagChallenge(CMagChallengeImpl):
    
    @raise_except_decorate(CMagChallInitError)
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

    @raise_except_decorate(CMagChallCreateError)
    def create_file(self, *args, **kwargs):
        return self.file_manager.create_file(*args, **kwargs)

    @raise_except_decorate(CMagChallAddError)
    def add_file(self, *args, **kwargs):
        return self.file_manager.add_file(*args, **kwargs)

    @raise_except_decorate(CMagChallGetError)
    def get_file(self, *args, **kwargs):
        return self.file_manager.get_file(*args, **kwargs)

    @raise_except_decorate(CMagChallGetByPathError)
    def get_file_by_path(self, *args, **kwargs):
        return self.file_manager.get_file_by_path(*args, **kwargs)

    @raise_except_decorate(CMagChallListError)
    def list_files(self, *args, **kwargs):
        return self.file_manager.list_files(*args, **kwargs)

    @raise_except_decorate(CMagChallRemoveError)
    def remove_file(self, *args, **kwargs):
        return self.file_manager.remove_file(*args, **kwargs)