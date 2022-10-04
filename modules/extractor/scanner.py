from cmag.modules import CMagChallScanner

class ArchiveFilesScanner(CMagChallScanner):
    name='extractor.scanner'
    def run(self, chall_id: str):
        challenge = self.project.challenge(chall_id)
        for file_id in challenge.files:
            file_path = challenge.file(file_id)
            for mod in self.project.mods.file_extractors:
                if mod.check(file_path):
                    self.project.scan_query(chall_id, mod.run, chall_id, file_id)