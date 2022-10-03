import pytest
from mods import (mod01, mod02, mod03, mod04, mod05, mod06, mod07, mod08)

import pathlib

from cmag.manager import CMagProject
from cmag.modules import (
    CMagModuleLoader,
    CMagModuleBase,
    CMagInitialScanner,
    CMagChallScanner,
    CMagFileScanner,
    CMagFileExtractor
)

@pytest.fixture
def loader():
    return CMagModuleLoader(None, pathlib.Path(__file__).parent / 'mods.py')

def test00_loader(loader: CMagModuleLoader):
    assert isinstance(loader, CMagModuleLoader)

def test01_mods(loader: CMagModuleLoader):

    testcases = {
        CMagModuleBase     : [mod01, mod02, mod03, mod04, mod05, mod06, mod07, mod08],
        CMagChallScanner   : [mod01],
        CMagInitialScanner : [mod02],
        CMagFileScanner    : [mod03, mod04, mod05],
        CMagFileExtractor  : [mod06, mod07, mod08]
    }

    for basecls, expected in testcases.items():
        for m in expected:
            found = False
            for l in loader.mods(basecls):
                found |= m.name == l.name
            assert found


def test02_mod_properties(loader: CMagModuleLoader):

    testcases = {
        'all'                : [mod01, mod02, mod03, mod04, mod05, mod06, mod07, mod08],
        'challenge_scanners' : [mod01],
        'initial_scanners'   : [mod02],
        'file_scanners'      : [mod03, mod04, mod05],
        'file_extractors'    : [mod06, mod07, mod08]
    }

    for attrname, expected in testcases.items():
        for m in expected:
            found = False
            for l in getattr(loader, attrname):
                found |= m.name == l.name
            assert attrname and found

def test03_file_mod_of(loader: CMagModuleLoader):
    
    testcases = {
        CMagFileScanner: {
            'a': set([mod03, mod04]),
            'b': set([mod03, mod05]),
            'c': set([mod03       ]),
            'd': set([            ]),
        },
        CMagFileExtractor: {
            'a': set([mod06, mod07]),
            'b': set([mod06, mod07]),
            'c': set([mod06, mod08]),
            'd': set([mod06       ])
        }
    }

    for basecls, testcase in testcases.items():
        for target, expected in testcase.items():
            result = set([m.name for m in loader.file_mods_of(target, basecls)])
            expect = set([e.name for e in expected])
            assert result == expect

def test04_find_mod_by_name(loader: CMagModuleLoader):
    for mod in [mod01, mod02, mod03, mod04, mod05, mod06, mod07, mod08]:
        assert loader.find_mod_by_name(mod.name)
