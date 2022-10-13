import secrets
import random
import hashlib
import pytest

from pathlib import Path
from cmag.project.project import CMagProject
from cmag.challenge.challenge import CMagChallenge
from cmag.challenge.manager import CMagChallengeManager
from cmag.file import CMagFile, CMagFileManager

@pytest.fixture
def tmp_path_str(tmp_path):
    return str(tmp_path)


@pytest.fixture
def file(tmp_path_str) :
    project = CMagProject(tmp_path_str)
    challmanager = CMagChallengeManager(project)
    challmanager.add_challenge('a')
    challenge = CMagChallenge(project, 1)
    return CMagFile(project, challenge, 1)

class Test00File:
    def test00_file_isinstance(self, file) :
        assert isinstance(file, CMagFile) is True


@pytest.fixture
def filemanager(tmp_path_str) :
    project = CMagProject(tmp_path_str)
    challmanager = CMagChallengeManager(project)
    challmanager.add_challenge('a')
    challenge = CMagChallenge(project, 1)
    return CMagFileManager(project, challenge)

class Test01FileManager:
    def test01_isinstance(self, filemanager) :
        assert isinstance(filemanager, CMagFileManager) is True

    def test01_abs_path(self, filemanager, tmp_path) :
        abspath = filemanager.abspath('./')
        assert abspath.is_absolute() is True
        abspath = filemanager.abspath(tmp_path)
        assert abspath.is_absolute() is True

    def test01_rel_path(self, filemanager, tmp_path) :
        relpath = filemanager.relpath('./')
        assert relpath == Path('./')
        relpath = filemanager.relpath(tmp_path)
        assert relpath is None

    def test01_make_file(self, filemanager, tmp_path) :
        randomfiles = make_random_files_at(tmp_path)
        assert filemanager.create_file(tmp_path) is None
        for _ in range(random.randrange(1, 5)) : #create_file
            file_name = secrets.token_hex(16)
            filemanager.create_file(file_name)
            assert (filemanager.path/file_name).is_file() is True
        for p, _, h in randomfiles : #add_file
            filemanager.add_file(p)
            assert (filemanager.path/p.name).is_file() is True
            with open((filemanager.path/p.name), 'rb') as f:
                assert h == hashlib.md5(f.read()).digest()

    def test01_doubly_add(self, filemanager, tmp_path) :
        p, d, h = make_random_file_at(tmp_path)
        filemanager.add_file(p)
        with pytest.raises(Exception) as IntegrityError :
            filemanager.add_file(p)

    def test01_doubly_create(self, filemanager) :
        filemanager.create_file('a')
        with pytest.raises(Exception) as IntegrityError :
            filemanager.create_file('a')

    def test01_not_exist_get(self, filemanager, tmp_path) :
        filemanager.create_file('a')
        filemanager.get_file_record_by_id(1)
        with pytest.raises(Exception) as CMagFileModelDoesNotExist :
            filemanager.get_file_record_by_id(2)
            filemanager.get_file_by_path(tmp_path / 'b')

    def test01_list(self, filemanager) :
        from string import ascii_lowercase
        for c in ascii_lowercase:
            filemanager.create_file(c)
        assert [file.path for file in filemanager.list_files()] == list(ascii_lowercase)

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

def make_random_file_at(tmp_path: Path):
    filepath = tmp_path / secrets.token_hex(16)
    filedata = secrets.token_bytes(random.randint(0, 0x1000))
    filehash = hashlib.md5(filedata).digest()
    with open(filepath, 'wb') as f:
        f.write(filedata)
    return filepath, filedata, filehash