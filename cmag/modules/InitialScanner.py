from cmag.modules import CMagInitialScanner, CMagChallScanner
from cmag.manager import CMagProjectImpl

class InitialFilesScanner(CMagInitialScanner):
    name='scanner.initial.files'
    def run(self, chall_id: str):
        mod = self.project.mods.find_mod_by_name('extractor.scanner')
        self.project.scan_query(chall_id, mod.run, chall_id)

def init(project: CMagProjectImpl):
    return [InitialFilesScanner(project)]