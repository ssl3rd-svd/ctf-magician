import typing
if typing.TYPE_CHECKING:
    from typing import Any, Dict, List, Optional
    from cmag.project import CMagProject
    from cmag.file import CMagFile

from .challenge_impl import CMagChallengeImpl
from .exceptions import *

class CMagChallenge(CMagChallengeImpl):

    def exception_handler(self, e):
        # TODO:
        pass

    @ExceptionDecorator(CMagChallengeImplFailed, exception_handler)
    def __init__(self, project: CMagProject, id: int):
        super().__init__(project, id)

    @ExceptionDecorator(CMagChallengeImplGetError, exception_handler)
    def get_record(self):
        return super().get_record()

    @ExceptionDecorator(CMagChallengeImplCreateError, exception_handler)
    def create_directory(self, *args, **kwargs) -> Optional[CMagFile]:
        return super().create_directory(*args, **kwargs)
    
    @ExceptionDecorator(CMagChallengeImplCreateError, exception_handler)
    def add_directory(self, *args, **kwargs) -> Optional[CMagFile]:
        return super().add_directory(*args, **kwargs)

    @ExceptionDecorator(CMagChallengeImplCreateError, exception_handler)
    def create_file(self, *args, **kwargs) -> Optional[CMagFile]:
        return super().create_file(*args, **kwargs)

    @ExceptionDecorator(CMagChallengeImplCreateError, exception_handler)
    def add_file(self, *args, **kwargs) -> Optional[CMagFile]:
        return super().add_file(*args, **kwargs)

    @ExceptionDecorator(CMagChallengeImplGetError, exception_handler)
    def get_file_by_id(self, *args, **kwargs):
        return super().get_file_by_id(*args, **kwargs)

    @ExceptionDecorator(CMagChallengeImplGetError, exception_handler)
    def get_file_by_path(self, *args, **kwargs):
        return super().get_file_by_path(*args, **kwargs)

    @ExceptionDecorator(CMagChallengeImplSelectError, exception_handler)
    def list_files(self, *args, **kwargs):
        return super().list_files(*args, **kwargs)

    @ExceptionDecorator(CMagChallengeImplDeleteError, exception_handler)
    def remove_file(self, *args, **kwargs):
        return super().remove_file(*args, **kwargs)