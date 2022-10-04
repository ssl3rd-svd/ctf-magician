from cmag.plugin.basecls import *

class InitialScannerSample(CMagInitialScanner):
    name = 'sample.initial'
    def run(self, chall_id: str):
        assert chall_id

class ChallengeScannerSample(CMagChallengeScanner):
    name = 'sample.challenge'
    def run(self, chall_id: str):
        assert chall_id

class FileExtractorSample(CMagFileExtractor):
    name = 'sample.file.extractor'
    def check(self, path: str):
        assert path
    def run(self, chall_id: str, file_id: int):
        assert chall_id
        assert file_id != None

class FileScannerSample(CMagFileScanner):
    name = 'sample.file.scanner'
    def check(self, path: str):
        assert path
    def run(self, chall_id: str, file_id: int):
        assert chall_id
        assert file_id != None

def init(project):
    return [
        InitialScannerSample(project),
        ChallengeScannerSample(project),
        FileExtractorSample(project),
        FileScannerSample(project),
    ]