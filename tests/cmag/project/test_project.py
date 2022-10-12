import pytest

from cmag.project import CMagProject
from cmag.database import CMagDatabase
from cmag.challenge.manager import CMagChallengeManager, CMagChallenge
from cmag.plugin.manager import CMagPluginManager

class Test00CMagProjectInit:
    def test00_init(self, tmp_path):
        assert tmp_path.is_dir() is True
        assert tmp_path.exists() is True
        project = CMagProject(tmp_path)
        assert project.path.exists() is True

    def test00_init_not_exist(self, tmp_path):
        not_exist_tmp_path = tmp_path / "not_exist"
        assert not_exist_tmp_path.exists() is False
        project = CMagProject(not_exist_tmp_path)
        assert project.path.exists() is True

    def test00_init_empty_string(self):
        empty_string = ""
        # this makes project directory at "."
        project = CMagProject(empty_string)
        assert project.path.exists() is True


class Test01ProjectDB:
    def test01_db_isinstance(self, tmp_path):
        project = CMagProject(tmp_path)
        assert isinstance(project.db, CMagDatabase) is True
        assert (project.path / "project.db").is_file() is True

@pytest.fixture
def project(tmp_path):
    return CMagProject(tmp_path)

class Test02ProjectChallengeManager:
    def test02_challenge_manager_isinstance(self, project):
        assert isinstance(project.challenge_manager, CMagChallengeManager) is True

    def test02_challenge_manager_add_get(self, project):
        assert isinstance(project.add_challenge('foo'), CMagChallenge) is True
        assert project.get_challenge_by_id(1).id == project.get_challenge_by_name('foo').id
