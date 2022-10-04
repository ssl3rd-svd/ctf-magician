from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import List
    from cmag.manager import CMagProjectImpl

from pathlib import Path
from importlib import import_module
from secrets import token_hex

from cmag.modules import (
    CMagModuleBase,
    CMagInitialScanner,
    CMagChallScanner,
    CMagFileScanner,
    CMagFileExtractor
)

class CMagModuleLoader:
    
    def __init__(self, project: CMagProjectImpl, modules_path: List[Path] = [], modules_name: List[str] = []):
        self._modules = []
        if modules_path:
            self._modules.extend(CMagModuleLoader.load_by_path(project, modules_path))
        if modules_name:
            self._modules.extend(CMagModuleLoader.load_by_name(project, modules_name))

    def load_by_path(project: CMagProjectImpl, modules_path: List[Path]):
    
        if not modules_path and not Path(modules_path).exists():
            raise FileNotFoundError

        modules = []

        for path in modules_path:

            target = Path(path)
        
            if target.name.endswith('.py'):
                name = target.stem
            else:
                name = target.name

            __import__("sys").path.append(target.parent)
            module = __import__(name)
        
            if not hasattr(module, 'init'):
                raise Exception

            modules.extend(module.init(project))

        for mod in modules:
            if not isinstance(mod, CMagModuleBase):
                raise Exception

        return modules

    def load_by_name(project: CMagProjectImpl, module_name: str | List[str]):

        if type(module_name) == str:

            # module = __import__(module_name)
            module = import_module(module_name, module_name.split(".")[-1])
            if not hasattr(module, 'init'):
                raise Exception

            mods = module.init(project)
            for mod in mods:
                if not isinstance(mod, CMagModuleBase):
                    raise Exception

            return mods

        modules = []
        for name in module_name:
            modules.extend(CMagModuleLoader.load_by_name(project, name))

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
