from pathlib import Path
from importlib.util import spec_from_file_location, module_from_spec
from typing import List

from cmag.manager import CMagProjectImpl
from cmag.modules import CMagModuleBase, CMagInitialScanner, CMagChallScanner, CMagFileScanner
from cmag.modules.Base import CMagFileExtractor

class CMagModuleLoader:
    
    def __init__(self, project: CMagProjectImpl, path: Path):
        self._modules = self.load(project, path)

    def load(project: CMagProjectImpl, path: Path):
        
        spec = spec_from_file_location(path)
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

    def file_scanners_of(self, target: str) -> List[CMagFileScanner]:
        
        ret = []
        
        for mod in self.file_scanners:
            if mod.target == '*':
                ret.append(mod)
                continue
            if target in mod.target.split(';'):
                ret.append(mod)
                continue
        
        return ret

    def file_extractors_of(self, target: str) -> List[CMagFileExtractor]:

        ret = []
        
        for mod in self.file_extractors:
            if mod.target == '*':
                ret.append(mod)
                continue
            if target in mod.target.split(';'):
                ret.append(mod)
                continue
        
        return ret

    def find_mod_by_name(self, name: str) -> CMagModuleBase:
        for mod in self.all:
            if mod.name == name:
                return mod
        return None