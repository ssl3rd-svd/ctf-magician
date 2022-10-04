from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cmag.project import CMagProject

from .PluginBase import CMagPluginBase as plugin

class CMagInitialScanner(plugin):
    def run(self, chall_id: str):
        raise NotImplementedError