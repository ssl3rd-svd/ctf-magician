import pytest
import os
import sys
from logging import Logger

from cmag.project import CMagProject
from cmag.database import CMagDatabase
from cmag.interface.logger import CMagLogger
from cmag.plugin.manager import CMagPluginManager
from cmag.challenge.manager import CMagChallengeManager, CMagChallenge

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
        os.remove('project.db')

    def test00_init_log_log_to_file(self, tmp_path):
        log_file = tmp_path / 'test00_init_log_to_file.log'
        project = CMagProject(tmp_path, log_to_file=log_file)
        assert log_file.is_file() is True

class Test01ProjectDB:
    def test01_db_isinstance(self, tmp_path):
        project = CMagProject(tmp_path)
        assert isinstance(project.db, CMagDatabase) is True
        assert (project.path / 'project.db').is_file() is True

@pytest.fixture
def project(tmp_path):
    return CMagProject(tmp_path)

class Test02Logger:
    def test02_logger_isinstance(self, project):
        assert isinstance(project.logger, CMagLogger) is True

    def test02_log_isinstance(self, project):
        assert isinstance(project.log, Logger) is True

class Test03PluginManager:
    def test02_plugin_manager_isinstance(self, project):
        assert isinstance(project.plugin_manager, CMagPluginManager) is True

class Test04ProjectChallengeManager:
    def test04_challenge_manager_isinstance(self, project):
        assert isinstance(project.challenge_manager, CMagChallengeManager) is True
