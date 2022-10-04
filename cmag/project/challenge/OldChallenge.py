from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Dict, List
    from cmag.project import CMagProject

raise DeprecationWarning

import copy
import shutil

from io import RawIOBase
from secrets import token_hex
from pathlib import Path

from cmag.project.challenge import CMagChallengeImpl
from cmag.project.exception import CMagChallIDExists, CMagChallIDNotFound

class CMagChallenge:

    CATEGORIES = {
        'pwn'   : 1,
        'rev'   : 2,
        'misc'  : 3,
        ''      : None
    }

    def new(project: CMagProject, files=[]):

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
