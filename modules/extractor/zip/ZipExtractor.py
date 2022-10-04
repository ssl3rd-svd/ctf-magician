from cmag.modules import CMagFileExtractor

class CMagZipExtractor(CMagFileExtractor):

    name='extractor.zip'
    target='zip'

    def check(self, path: str):
        with open(path, 'rb') as f:
            return f.read(2) == b'PK'

    def run(self, chall_id: str, file_id: int, *args, **kwargs):
        import zipfile
        challenge = self.project.challenge(chall_id)
        file_path = challenge.file(file_id)
        with zipfile.ZipFile(file_path, 'r') as zip:
            for name in zip.namelist():
                with zip.open(name) as file:
                    challenge.add_file(name, file)