from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    from typing import Any, Dict, List
    from cmag.challenge import CMagChallenge

from .project_impl import CMagProjectImpl
from .exceptions import *

class CMagProject(CMagProjectImpl):
    
    def exception_handler(self, e):
        # TODO:
        pass

    @ExceptionDecorator(CMagProjectFailed, exception_handler)
    def __init__(self, project_dir: str):
        super().__init__(project_dir)

    @ExceptionDecorator(CMagProjectImplAddError, exception_handler)
    def add_challenge(self, *args, **kwargs) -> CMagChallenge:
        return super().add_challenge(*args, **kwargs)
    
    @ExceptionDecorator(CMagProjectImplGetError, exception_handler)
    def get_challenge_by_id(self, *args, **kwargs) -> CMagChallenge:
        return super().get_challenge_by_id(*args, **kwargs)

    @ExceptionDecorator(CMagProjectImplGetError, exception_handler)
    def get_challenge_by_name(self, *args, **kwargs) -> CMagChallenge:
        return super().get_challenge_by_name(*args, **kwargs)

    @ExceptionDecorator(CMagProjectImplListError, exception_handler)
    def list_challenges(self, *args, **kwargs) -> Dict[int, str]:
        return super().list_challenges(*args, **kwargs)

    @ExceptionDecorator(CMagProjectImplRemoveError, exception_handler)
    def remove_challenge(self, *args, **kwargs):
        return super().remove_challenge(*args, **kwargs)

    @ExceptionDecorator(CMagProjectImplAddError, exception_handler)
    def add_plugin(self, *args, **kwargs):
        return super().add_plugin(*args, **kwargs)

    @ExceptionDecorator(CMagProjectImplEnableError, exception_handler)
    def enable_plugin(self, *args, **kwargs):
        return super().enable_plugin(*args, **kwargs)

    @ExceptionDecorator(CMagProjectImplDisableError, exception_handler)
    def disable_plugin(self, *args, **kwargs):
        return super().disable_plugin(*args, **kwargs)

    @ExceptionDecorator(CMagProjectImplLoadError, exception_handler)
    def load_all(self, *args, **kwargs):
        return super().load_all(*args, **kwargs)

    @ExceptionDecorator(CMagProjectImplLoadError, exception_handler)
    def load_plugin_once(self, *args, **kwargs):
        return super().load_plugin_once(*args, **kwargs)

    @ExceptionDecorator(CMagProjectImplLoadError, exception_handler)
    def load_plugin(self, *args, **kwargs):
        return super().load_plugin(*args, **kwargs)

    @ExceptionDecorator(CMagProjectImplGetError, exception_handler)
    def get_loaded_plugin(self, *args, **kwargs):
        return super().get_loaded_plugin(*args, **kwargs)

    @ExceptionDecorator(CMagProjectImplListError, exception_handler)
    def list_plugins(self, *args, **kwargs):
        return super().list_plugins(*args, **kwargs)

    @ExceptionDecorator(CMagProjectImplListError, exception_handler)
    def list_loaded_plugins(self, *args, **kwargs):
        return super().list_loaded_plugins(*args, **kwargs)

    @ExceptionDecorator(CMagProjectImplSaveError, exception_handler)
    def save_loaded_plugin_options(self, *args, **kwargs):
        return super().save_loaded_plugin_options(*args, **kwargs)

    @ExceptionDecorator(CMagProjectImplUnloadError, exception_handler)
    def unload_plugin_once(self, *args, **kwargs):
        return super().unload_plugin_once(*args, **kwargs)

    @ExceptionDecorator(CMagProjectImplUnloadError, exception_handler)
    def unload_plugin(self, *args, **kwargs):
        return super().unload_plugin(*args, **kwargs)