from __future__ import annotations
if __import__("typing").TYPE_CHECKING:
    from cmag.project import CMagProject

from cmag.plugin.basecls import CMagInitialScanner

class InitialFilesScanner(CMagInitialScanner):
    name='scanner.initial.files'
    def run(self, chall_id: str):
        mod = self.project.mods.find_mod_by_name('extractor.scanner')
        self.project.scan_query(chall_id, mod.run, chall_id)

def init(project: CMagProject):
    return [InitialFilesScanner(project)]