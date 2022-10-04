import pytest

from tempfile import mkdtemp
from pathlib import Path

# @pytest.fixture
# def workdir():
#     return str(Path(mkdtemp()))

@pytest.fixture
def modspath():
    return str(Path(__file__).parent / 'mods')
