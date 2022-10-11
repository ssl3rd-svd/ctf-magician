
# from cmag.database import CMagDatabase
# from cmag.challenge import CMagChallenge
# from cmag.challenge.manager import CMagChallengeManager
# from cmag.plugin.manager import CMagPluginManager

from cmag.project import CMagProject

# import pytest

def test_CMagProject():
    test_dir = "/tmp/project"
    project = CMagProject(test_dir)
    assert project != None