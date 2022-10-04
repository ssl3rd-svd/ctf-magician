from __future__ import annotations
import typing

if typing.TYPE_CHECKING:
    from cmag.manager import CMagProjectImpl

import pytest

from pathlib                import Path
from cmag.manager           import CMagProject, CMagProjectDatabase, CMagProjectConfig
from cmag.manager.exception import CMagConfigNotFound

@pytest.fixture
def project(tmp_path, modspath):
    return CMagProject.new(tmp_path / 'project', {'modules': [modspath]})

class Test00ProjectInterface:

    def test01_new(self, tmp_path, modspath):

        try:
            assert not CMagProject.new(tmp_path, {})
        except FileExistsError:
            pass

        try:
            assert not CMagProject.new(tmp_path / 'project01')
        except FileNotFoundError as e:
            pass
        
        try:
            CMagProject.new(tmp_path / 'project02', {'modules': []})
        except CMagConfigNotFound as e:
            assert e.cfgkey == 'modules'

        CMagProject.new(tmp_path / 'project03', {'modules': [modspath]})

    def test01_load(self, tmp_path, modspath):

        try:
            assert not CMagProject.load(tmp_path / 'project', {'modules': [modspath]})
        except FileNotFoundError:
            pass

        CMagProject.new(tmp_path / 'project', {'modules': [modspath]})
        CMagProject.load(tmp_path / 'project', {'modules': [modspath]})

class Test01ProjectPath:

    def test01_dir(self, project: CMagProjectImpl, tmp_path):
        assert project.dir == (tmp_path / 'project')
        assert project.dir.is_dir()

    def test01_db_path(self, project: CMagProjectImpl, tmp_path: Path):
        assert project.db_path == (tmp_path / 'project' / 'project.sqlite3')
        assert project.db_path.is_file()

    def test01_cfg_path(self, project: CMagProjectImpl, tmp_path: Path):
        assert project.cfg_path == (tmp_path / 'project' / 'config.json')
        assert project.cfg_path.is_file()

    def test01_files_dir(self, project: CMagProjectImpl, tmp_path: Path):
        assert project.files_dir == (tmp_path / 'project' / 'files')
        assert project.files_dir.is_dir()

class Test02ProjectConfig:

    def test01_config(self, project: CMagProjectImpl):
        assert type(project.config) == CMagProjectConfig

class Test03ProjectDatabase:

    def test01_database(self, project: CMagProjectImpl):
        assert isinstance(project.database, CMagProjectDatabase)
        with project.database as db:
            db.Challenge.create_table()
            db.File.create_table()

class Test04ProjectChallenge:
    def test01_challenges(self, project: CMagProjectImpl):
        pass

class Test05ProjectMods:
    def test01_mods(self, project: CMagProjectImpl):
        pass