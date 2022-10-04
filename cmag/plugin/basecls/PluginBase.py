from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cmag.project import CMagProject

class CMagPluginBase:

    name = ''

    def __init__(self, project: CMagProject):
        
        if self.name == '':
            raise NotImplementedError

        self.project = project

    def check(self):
        raise NotImplementedError

    def run(self):
        raise NotImplementedError