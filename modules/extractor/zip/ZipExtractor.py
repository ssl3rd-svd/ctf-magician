from cmag.modules import CMagFileExtractor

class CMagZipExtractor(CMagFileExtractor):

    name='extractor.zip'
    target='zip'

    def check(self, path: str):
        with open(path, 'rb') as f:
            return f.read(2) == b'PK'

    def run(self, chall_id: str, file_id: int, *args, **kwargs):
        import zipfile
        challenge = self.project.challenges[chall_id]
        filepath = challenge.files[file_id]
        with zipfile.ZipFile(filepath, 'r') as zip:
            for name in zip.namelist():
                with zip.open(name) as file:
                    challenge.write_file(name, file)