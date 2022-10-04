from pathlib import Path
from io import RawIOBase
from shutil import copyfile, copyfileobj

class CMagFileManager:
    
    def __init__(self, challenge):
        
        self._challenge = challenge
        self._project = challenge.project

        if not self.dir.is_dir():
            self.dir.mkdir()

    @property
    def project(self):
        return self._project

    @property
    def challenge(self):
        return self._challenge

    @property
    def dir(self):
        return self.project.files_dir / self.challenge.id

    @property
    def ids(self):
        with self.project.database as db:
            return [r.id for r in db.Challenge.get(db.Challenge.id == self.id).files]

    @property
    def paths(self):
        with self.project.database as db:
            return [r.filepath for r in db.Challenge.get(db.Challenge.id == self.id).files]

    def id(self, path: Path):
        path = Path(path)
        if path.is_absolute():
            path = path.relative_to(self.dir)
        with self.project.database as db:
            file = db.File.get(db.File.filepath == str(path))
            return file.id

    def path(self, id: int):
        with self.project.database as db:
            file = db.File.get(db.File.id == id)
            return Path(file.filepath)

    def add(self, filepath: Path, srcobj: RawIOBase = None):

        filepath = Path(filepath)

        copy_dst = self.dir / filepath.name
        if copy_dst.is_file():
            raise FileExistsError

        if not srcobj:
            copyfile(filepath, copy_dst)
        else:
            with open(copy_dst, 'wb') as dstobj:
                copyfileobj(srcobj, dstobj)

        copied = copy_dst.relative_to(self.dir)

        with self.project.database as db:
            row = db.Challenge.get(db.Challenge.id == self.id)
            file = db.File.create(challenge=row, filepath=copied)
            file.save()

    def remove(self, id: int):
        with self.project.database as db:
            file = db.File.get(db.File.id == id)
            file.delete_instance()
