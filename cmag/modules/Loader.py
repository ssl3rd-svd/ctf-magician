from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import List
    from cmag.manager import CMagProjectImpl

from pathlib import Path
from importlib.util import spec_from_file_location, module_from_spec
from secrets import token_hex

from cmag.modules import (
    CMagModuleBase,
    CMagInitialScanner,
    CMagChallScanner,
    CMagFileScanner,
    CMagFileExtractor
)

class CMagModuleLoader:
    
    def __init__(self, project: CMagProjectImpl, path: Path):
        self._modules = CMagModuleLoader.load(project, path)

    def load(project: CMagProjectImpl, path: Path):
        
        if not path:
            raise FileNotFoundError

        spec = spec_from_file_location(token_hex(32), path)
        module = module_from_spec(spec)
        spec.loader.exec_module(module)
        
        if not hasattr(module, 'init'):
            raise Exception

        modules = module.init(project)

        for mod in modules:
            if not isinstance(mod, CMagModuleBase):
                raise Exception

        return modules

    @property
    def all(self) -> List[CMagModuleBase]:
        return self._modules

    @property
    def initial_scanners(self) -> List[CMagInitialScanner]:
        return self.mods(CMagInitialScanner)

    @property
    def challenge_scanners(self) -> List[CMagChallScanner]:
        return self.mods(CMagChallScanner)

    @property
    def file_scanners(self) -> List[CMagFileScanner]:
        return self.mods(CMagFileScanner)

    @property
    def file_extractors(self) -> List[CMagFileExtractor]:
        return self.mods(CMagFileExtractor)

    def mods(self, base_cls=None):
        if not base_cls:
            return self.all
        return [mod for mod in self.all if isinstance(mod, base_cls)]

    def file_mods_of(self, target: str, basecls=None):

        ret = []
        
        for mod in self.mods(basecls):
            if mod.target == '*':
                ret.append(mod)
            elif target in mod.target.split(';'):
                ret.append(mod)

        return ret

    def file_scanners_of(self, target: str) -> List[CMagFileScanner]:
        return self.file_mods_of(target, CMagFileScanner)

    def file_extractors_of(self, target: str) -> List[CMagFileExtractor]:
        return self.file_mods_of(target, CMagFileExtractor)

    def find_mod_by_name(self, name: str) -> CMagModuleBase:
        for mod in self.all:
            if mod.name == name:
                return mod
        return None
