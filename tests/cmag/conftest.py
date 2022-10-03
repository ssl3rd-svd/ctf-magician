import pytest

from tempfile import mkdtemp
from pathlib import Path

@pytest.fixture
def workdir():
    return Path(mkdtemp())

@pytest.fixture
def modspath():
    return Path(__file__).parent / 'mods.py'
