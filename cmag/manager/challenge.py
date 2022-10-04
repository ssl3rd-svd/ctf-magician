from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Dict, List
    from cmag.manager import CMagProjectImpl

import copy
import shutil

from io import RawIOBase
from secrets import token_hex
from pathlib import Path

from cmag.manager.exception import CMagChallIDExists, CMagChallIDNotFound

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
    def files(self) -> List[int]:
        with self.project.database as db:
            return [r.id for r in db.Challenge.get(db.Challenge.id == self.id).files]

    # file methods

    def file(self, id) -> Path:
        with self.project.database as db:
            return self.project.dir / Path(db.File.get(db.File.id == id).filepath)

    def add_file(self, filepath: Path, srcobj: RawIOBase = None):

        filepath = Path(filepath)

        copy_dst = self.files_dir / filepath.name
        if copy_dst.is_file():
            raise FileExistsError

        if not srcobj:
            shutil.copyfile(filepath, copy_dst)
        else:
            with open(copy_dst, 'wb') as dstobj:
                shutil.copyfileobj(srcobj, dstobj)

        copied = copy_dst.relative_to(self.project.dir)

        with self.project.database as db:
            chall_row = db.Challenge.get(db.Challenge.id == self.id)
            file = db.File.create(challenge=chall_row, filepath=copied)
            file.save()

    def upd_file(self):
        pass

    def del_file(self, id: int):
        with self.project.database as db:
            file = db.File.get(db.File.id == id)
            file.delete_instance()

    # scan methods

    def scan(self, *args, **kwargs):
        return self.project.scan_challenge(self.id, *args, **kwargs)

    def scan_query(self, *args, **kwargs):
        return self.project.scan_query(self.id, *args, **kwargs)

    def scan_query_next(self, *args, **kwargs):
        return self.project.scan_query_next(self.id, *args, **kwargs)

    def scan_cancel_after(self, *args, **kwargs):
        return self.project.scan_cancel_after(self.id, *args, **kwargs)

    def scan_cancel_all(self, *args, **kwargs):
        return self.project.scan_cancel_all(self.id, *args, **kwargs)

class CMagChallenge:

    CATEGORIES = {
        'pwn'   : 1,
        'rev'   : 2,
        'misc'  : 3,
        ''      : None
    }

    def new(project: CMagProjectImpl, files=[]):

        id = token_hex(16)
        if id in project.challenges:
            raise CMagChallIDExists(id=id)

        (project.files_dir / id).mkdir()

        # if files:
        #     copied_files = []
        #     for file in files:
        #         file_src = Path(file)
        #         file_name = file_src.name
        #         file_dst = files_dir / file_name
        #         shutil.copyfile(file_src, file_dst)
        #         copied_files.append(file_dst.relative_to(project.dir))

        with project.database as db:
            db.Challenge.create(id=id)

        chall_obj = CMagChallengeImpl(project, id)

        # if files:
        #     for file in files:
        #         chall_obj.add_file(file)

        return chall_obj

    def load(project, challenge_id):
        if challenge_id not in project.challenges:
            raise CMagChallIDNotFound(id=challenge_id)
        return CMagChallengeImpl(project, challenge_id)

    def guess_category(category: str) -> Dict[str, int]:
        category = category.lower()
        for ini, val in CMagChallenge.CATEGORIES.items():
            if category.startswith(ini):
                return ini, val
