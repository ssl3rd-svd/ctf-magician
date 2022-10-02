from cmag.modules import CMagChallScanner

class ArchiveFilesScanner(CMagChallScanner):
    name='extractor.scanner'
    def run(self, chall_id: str):
        challenge = self.project.challenges[chall_id]
        for fileid, path in challenge.files.items():
            for mod in self.project.mods.file_extractors:
                if mod.check(path):
                    self.project.scan_add(chall_id, mod.run, chall_id, fileid)