from __future__ import annotations
import typing

from cmag.manager.exception.ChallengeExc import CMagChallIDNotFound
if typing.TYPE_CHECKING:
    from cmag.manager import CMagProjectImpl

import pytest
import tempfile
import secrets
import random
import hashlib

from pathlib import Path
from cmag.manager import CMagProject, CMagChallenge

@pytest.fixture
def project(tmp_path, modspath):
    return CMagProject.new(tmp_path / 'project', {'modules': str(modspath)})

def make_random_files_at(tmp_path: Path):
    ret = []
    for _ in range(random.randrange(1, 16)):
        filepath = tmp_path / secrets.token_hex(16)
        filedata = secrets.token_bytes(random.randint(0, 0x1000))
        filehash = hashlib.md5(filedata).digest()
        with open(filepath, 'wb') as f:
            f.write(filedata)
        ret.append((filepath, filedata, filehash))
    return ret

class Test00ChallengeInterface:

    def test00_guess_category(self):
        for k, v in CMagChallenge.CATEGORIES.items():
            assert CMagChallenge.guess_category(k) == (k, v)
            assert CMagChallenge.guess_category(k.upper()) == (k, v)
            assert CMagChallenge.guess_category(k + 'able') == (k, v)

    def test01_new(self, project: CMagProjectImpl):
        chall = CMagChallenge.new(project)
        assert chall.id in project.challenges
        assert (project.files_dir / chall.id).is_dir()
        assert project.challenge(chall.id)

    def test01_load(self, project: CMagProjectImpl):
        try:
            assert not CMagChallenge.load(project, '1337')
        except CMagChallIDNotFound as e:
            assert e.id == '1337'

class Test02ChallengeFile:

    def test00_add_files_1(self, project: CMagProjectImpl, tmp_path: Path):

        random_files_1 = make_random_files_at(tmp_path)
        random_files_2 = make_random_files_at(tmp_path)

        chall = CMagChallenge.new(project)
        
        for p, _, _ in random_files_1:
            chall.add_file(p)
        for p, _, _ in random_files_2:
            with open(p, 'rb') as f:
                chall.add_file(p, f)

        for file_id in chall.files:

            file = chall.file(file_id)

            for p, d, h in random_files_1:
                if Path(p).name == file.name:
                    with file.open('rb') as f:
                        assert h == hashlib.md5(f.read()).digest()

            for p, d, h in random_files_2:
                if Path(p).name == file.name:
                    with file.open('rb') as f:
                        assert h == hashlib.md5(f.read()).digest()

    def test01_upd_file(self):
        pass

    def test01_del_file(self):
        pass