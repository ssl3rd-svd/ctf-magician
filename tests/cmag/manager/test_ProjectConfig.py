from pathlib import Path
import pytest
import secrets
import json

from cmag.manager import CMagProjectConfig

@pytest.fixture
def cfg_path(tmp_path):
    return tmp_path / (secrets.token_hex(8) + '.json')

@pytest.fixture
def cfg_data():
    return {
        'name': '',
        'modules': []
    }

def test00_init_from_file(cfg_path, cfg_data):

    with cfg_path.open('w') as f:
        json.dump(cfg_data, f)

    CMagProjectConfig(cfg_path)

def test00_init_and_save(cfg_path, cfg_data):

    cfg_data['name'] = 'hey'
    cfg = CMagProjectConfig(cfg_path, cfg_data)
    cfg.save()
    
    with cfg_path.open('r') as f:
        cfg_data = json.load(f)
    
    assert 'name' in cfg_data
    assert cfg_data['name'] == 'hey'

def test01_field_required(cfg_path, cfg_data):
    
    CMagProjectConfig(cfg_path, cfg_data)

    del cfg_data['modules']
    try:
        assert CMagProjectConfig(cfg_path, cfg_data) == None
    except KeyError:
        pass

def test02_field_default(cfg_path, cfg_data):
    cfg_data['name'] = 'hey'
    cfg = CMagProjectConfig(cfg_path, cfg_data)
    assert cfg['name'] == 'hey'
    cfg['name'] = 'hi'
    assert cfg['name'] == 'hi'

def test02_field_abspathlist(cfg_path, cfg_data):
    cfg_data['modules'] = ['a/b']
    cfg = CMagProjectConfig(cfg_path, cfg_data)
    assert str(cfg['modules'][0]) == str(Path('a/b').absolute())
    cfg['modules'] = ['c/d']
    assert str(cfg['modules'][0]) == str(Path('c/d').absolute())