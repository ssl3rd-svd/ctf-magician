from __future__ import annotations
import typing

if typing.TYPE_CHECKING:
    from cmag.manager import CMagProjectImpl

import pytest

from pathlib                import Path
from cmag.manager           import CMagProject, CMagProjectDatabase
from cmag.manager.exception import CMagConfigNotFound

@pytest.fixture
def project(workdir, modspath):
    return CMagProject.new(workdir / 'project', {'modules': str(modspath)})

class Test00ProjectInterface:

    def test01_new(self, workdir, modspath):
        
        workdir = Path(workdir)

        try:
            assert not CMagProject.new(workdir, {})
        except FileExistsError:
            pass

        try:
            assert not CMagProject.new(workdir / 'project01', {})
        except CMagConfigNotFound as e:
            assert e.cfgkey == 'modules'
        
        CMagProject.new(workdir / 'project02', {'modules': str(modspath)})

    def test01_load(self, workdir, modspath):

        workdir = Path(workdir)

        try:
            assert not CMagProject.load(workdir / 'project', {'modules': str(modspath)})
        except FileNotFoundError:
            pass

        CMagProject.new(workdir / 'project', {'modules': str(modspath)})
        CMagProject.load(workdir / 'project', {'modules': str(modspath)})

class Test01ProjectPath:

    def test01_dir(self, project: CMagProjectImpl, workdir: Path):
        assert project.dir == (workdir / 'project')
        assert project.dir.is_dir()

    def test01_db_path(self, project: CMagProjectImpl, workdir: Path):
        assert project.db_path == (workdir / 'project' / 'project.sqlite3')
        assert project.db_path.is_file()

    def test01_cfg_path(self, project: CMagProjectImpl, workdir: Path):
        assert project.cfg_path == (workdir / 'project' / 'config.json')
        assert project.cfg_path.is_file()

    def test01_files_dir(self, project: CMagProjectImpl, workdir: Path):
        assert project.files_dir == (workdir / 'project' / 'files')
        assert project.files_dir.is_dir()

class Test02ProjectConfig:

    def test01_config(self, project: CMagProjectImpl):
        assert type(project.config) == dict

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