import pytest

from cmag.project import CMagProject
from cmag.challenge.manager import CMagChallengeManager, CMagChallenge

@pytest.fixture
def tmp_path_str(tmp_path):
    return str(tmp_path)

@pytest.fixture
def challenge(tmp_path_str) :
    project = CMagProject(tmp_path_str)
    return CMagChallenge(project, 1)

class Test00Challenge:
    def test00_isinstance(self, challenge) :
        assert isinstance(challenge, CMagChallenge) is True

@pytest.fixture
def challmanager(tmp_path_str) :
    project = CMagProject(tmp_path_str)
    return CMagChallengeManager(project)

class Test01ChallengeManager:
    def test01_isinstance(self, challmanager):
        assert isinstance(challmanager, CMagChallengeManager) is True

    def test01_get_set(self, challmanager):
        chall = challmanager.add_challenge("a")
        assert isinstance(chall, CMagChallenge) is True
        got_chall = challmanager.get_challenge(1)
        assert chall.id == got_chall.id
        assert chall.name == got_chall.name

    def test01_doubly_add(self, challmanager):
        challmanager.add_challenge('a')
        challmanager.add_challenge('a')

    def test01_not_exist_get(self, challmanager):
        challmanager.add_challenge('a')
        challmanager.get_challenge_by_name('b')

    def test01_list(self, challmanager):
        from string import ascii_lowercase
        for c in ascii_lowercase:
            challmanager.add_challenge(c)
        assert [chall.name for chall in challmanager.list_challenges()] == list(ascii_lowercase)

    def test01_doubly_remove(self, challmanager):
        challmanager.add_challenge('a')
        challmanager.remove_challenge(1)
        challmanager.remove_challenge(1)