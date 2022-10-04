import pytest

from cmag.project.config import CMagConfig
from cmag.project.config import CMagFieldTypes as fieldtypes

@pytest.fixture
def fields():

    class f_string(fieldtypes.string):
        name = 'field.string'
        desc = 'string type field for test.'

    class f_integer(fieldtypes.integer):
        name = 'field.integer'
        desc = 'integer type field for test.'

    class f_abspath(fieldtypes.abspath):
        name = 'field.abspath'
        desc = 'absolute path type field for test.'

    class f_abspathlist(fieldtypes.abspathlist):
        name = 'field.abspathlist'
        desc = 'absolute path list type for test.'

    return [f_string, f_integer, f_abspath, f_abspathlist]

class Test0CMagConfig:
        
    def test0_fields(self, fields):
        assert issubclass(fields[0], fieldtypes.string)
        assert fields[0].name == 'field.string'
        assert fields[0].desc == 'string type field for test.'

    def test01_init(self, fields, tmp_path):

        f_string_val = 'teststring'
        f_integer_val = 1234
        f_abspath_val = '/etc/passwd'
        f_abspathlist_val = ['/etc/passwd', '/etc/shadow']

        config = CMagConfig(fields, tmp_path / 'test01_init.json', {
            'field.string'  : f_string_val,
            'field.integer' : f_integer_val,
            'field.abspath' : f_abspath_val,
            'field.abspathlist': f_abspathlist_val
        })

        assert config
        assert config['field.string'] == f_string_val
        assert config['field.integer'] == f_integer_val
        assert str(config['field.abspath']) == f_abspath_val
        assert len([p for i, p in enumerate(config['field.abspathlist']) if str(p) == f_abspathlist_val[i]]) == len(f_abspathlist_val)

    def test2_load_and_save(self, fields, tmp_path):

        config = CMagConfig(fields, tmp_path / (__name__ + '.json'), {'field.string': 'string'})
        assert config.path.is_file()

        config = CMagConfig(fields, tmp_path / (__name__ + '.json'))
        assert config['field.string'] == 'string'

    def test3_required_field(self, fields, tmp_path):
        
        fields[0].required = True

        try:
            config = CMagConfig(fields, tmp_path / (__name__ + '.json'), {'field.integer': 0})
            assert not config.required_fields
        except KeyError:
            pass

        config = CMagConfig(fields, tmp_path / (__name__ + '.json'), {'field.string': 'hello'})
        assert 'field.string' in config.required_fields