from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Dict
    from cmag.manager import CMagProjectImpl

import copy
import shutil

from io import RawIOBase
from secrets import token_hex
from pathlib import Path

class CMagChallengeImpl:

    def __init__(self, project: CMagProjectImpl, challenge_id: str):
        self._project = project
        self._id      = challenge_id

    @property
    def project(self): return self._project

    @property
    def id(self): return self._id

    @property
    def files_dir(self): return self.project.files_dir / self.id

    @property
    def files(self) -> Dict[int, Path]:
        files = {}
        with self.project.database as db:
            for row in db.Challenge.get(db.Challenge.id == self.id).files:
                files[row.id] = row.filepath
        return files

    # file methods

    def add_file(self, filepath: Path):

        filepath = Path(filepath)
        if filepath.is_absolute():
            raise Exception

        copy_src = filepath
        copy_dst = self.files_dir / filepath.name
        shutil.copyfile(copy_src, copy_dst)

        copied = copy_dst.relative_to(self.project.dir)

        with self.project.database as db:
            chall_row = db.Challenge.get(db.Challenge.id == self.id)
            file = db.File.create(challenge=chall_row, filepath=copied)
            file.save()

    def write_file(self, filepath: Path, srcfile: RawIOBase):

        filepath = Path(filepath)
        if filepath.is_absolute():
            raise Exception

        copy_dst = self.files_dir / filepath.name
        with open(copy_dst, 'wb') as dstfile:
            shutil.copyfileobj(srcfile, dstfile)

    def upd_file(self):
        pass

    def del_file(self, id: int):
        with self.project.database as db:
            file = db.File.get(db.File.id == id)
            file.delete_instance()

class CMagChallenge:

    CATEGORIES = {
        'pwn'   : 1,
        'rev'   : 2,
        'misc'  : 3,
        ''      : None
    }

    def new(project: CMagProjectImpl, *args, **kwargs):

        id = token_hex(16)

        files_dir = project.files_dir / id
        if files_dir.is_dir():
            raise FileExistsError(f"{files_dir} exists.")

        if 'files' in kwargs:
            files = []
            for file in kwargs['files']:
                file_src = Path(file)
                file_name = file_src.name
                file_dst = files_dir / file_name
                shutil.copyfile(file_src, file_dst)
                files.append(file_dst.relative_to(project.dir))

        create = copy.deepcopy(kwargs)
        create['id'] = id
        create['category'] = CMagChallenge.guess_category(kwargs['category'])[1]

        with project.database as db:
            
            chall = db.Challenge.create(**create)
            chall.save()

            for file in files:
                file = db.File.create(challenge=chall, filepath=file)
                file.save()

        return CMagChallengeImpl(project, id)

    def load(project, challenge_id):
        return CMagChallengeImpl(project, challenge_id)

    def guess_category(category):
        category = category.lower()
        for ini, val in CMagChallenge.CATEGORIES:
            if category.startswith(ini):
                return ini, val
