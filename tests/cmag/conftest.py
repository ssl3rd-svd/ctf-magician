import pytest

from tempfile import mkdtemp
from pathlib import Path

@pytest.fixture
def workdir():
    return Path(mkdtemp())