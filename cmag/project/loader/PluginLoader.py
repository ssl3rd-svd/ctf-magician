from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import List
    from cmag.project import CMagProject
    from pathlib import Path

from pathlib import Path
from importlib import import_module
from secrets import token_hex

from cmag.plugin.basecls import (
    CMagPluginBase,
    CMagInitialScanner,
    CMagChallengeScanner,
    CMagFileScanner,
    CMagFileExtractor
)

class CMagPluginLoader:
    
    def __init__(self, project: CMagProject, plugins_path: List[Path] = [], plugins_name: List[str] = []):
        self._plugins = []
        if plugins_path:
            self._plugins.extend(CMagPluginLoader.load_by_path(project, plugins_path))
        if plugins_name:
            self._plugins.extend(CMagPluginLoader.load_by_name(project, plugins_name))

    def load_by_path(project: CMagProject, plugins_path: List[Path | str]):

        plugins = []

        for path in plugins_path:

            target = Path(path)
        
            if target.name.endswith('.py'):
                name = target.stem
            else:
                name = target.name

            # TODO: need to imporve this.
            __import__("sys").path.append(target.parent)
            module = __import__(name)
    
            if hasattr(module, 'init'):
                pins = module.init(project)
                for p in pins:
                    if isinstance(p, CMagPluginBase):
                        plugins.append(p)

        return plugins

    def load_by_name(project: CMagProject, plugins_name: str | List[str]):

        plugins = []

        if type(plugins_name) == str:
            module = import_module(plugins_name, plugins_name.split(".")[-1])
            if hasattr(module, 'init'):
                for plugin in module.init(project):
                    if isinstance(plugin, CMagPluginBase):
                        plugins.append(plugin)

        elif type(plugins_name) == list:
            for name in plugins_name:
                plugins.extend(CMagPluginLoader.load_by_name(project, name))

        else:
            raise NotImplementedError

        return plugins

    @property
    def all(self) -> List[CMagPluginBase]:
        return self._plugins

    @property
    def initial_scanners(self) -> List[CMagInitialScanner]:
        return self.get_plugins_of(CMagInitialScanner)

    @property
    def challenge_scanners(self) -> List[CMagChallengeScanner]:
        return self.get_plugins_of(CMagChallengeScanner)

    @property
    def file_scanners(self) -> List[CMagFileScanner]:
        return self.get_plugins_of(CMagFileScanner)

    @property
    def file_extractors(self) -> List[CMagFileExtractor]:
        return self.get_plugins_of(CMagFileExtractor)

    def get_plugins_of(self, base_cls=None):
        if not base_cls:
            return self.all
        return [mod for mod in self.all if isinstance(mod, base_cls)]

    def find_file_plugins_of(self, target: str, base_cls=None):

        ret = []
        
        for mod in self.get_plugins_of(base_cls):
            if mod.target == '*':
                ret.append(mod)
            elif target in mod.target.split(';'):
                ret.append(mod)

        return ret

    def find_file_scanners_of(self, target: str) -> List[CMagFileScanner]:
        return self.find_file_plugins_of(target, CMagFileScanner)

    def find_file_extractors_of(self, target: str) -> List[CMagFileExtractor]:
        return self.find_file_plugins_of(target, CMagFileExtractor)

    def find_plugin_by_name(self, name: str) -> CMagPluginBase:
        for mod in self.all:
            if mod.name == name:
                return mod
        return None
