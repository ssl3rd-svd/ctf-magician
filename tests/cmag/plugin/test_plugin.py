import pytest
from cmag.plugin.plugin import CMagPlugin
from cmag.project.project import CMagProject
from cmag.plugin.manager import CMagPluginManager
from cmag.plugin.model import CMagPluginModel
from cmag.builtin.hello import HelloPlugin

@pytest.fixture
def tmp_path_str(tmp_path):
    return str(tmp_path)


@pytest.fixture
def plugin(tmp_path_str) :
    project = CMagProject(tmp_path_str)
    return CMagPlugin(project)

class Test01CMagPlugin :
    def test00_isinstance(self, plugin) :
        assert isinstance(plugin, CMagPlugin) is True

    def test01_not_exist(self, plugin) :
        assert plugin.is_loaded_once() is True
        assert plugin.load_options() is False
        assert plugin.save_options_to_db() is False


@pytest.fixture
def plugin_manager(tmp_path_str) :
    project = CMagProject(tmp_path_str)
    return CMagPluginManager(project)         

class Test00CMagPluginManager :
    def test00_isinstance(self, plugin_manager) :
        assert isinstance(plugin_manager, CMagPluginManager) is True

    def test00_not_exist_id(self, plugin_manager) :
        assert plugin_manager.load_plugin(1) is None
        assert plugin_manager.get_loaded_plugin(1) is None
        assert plugin_manager.enable_plugin(1) is False
        assert plugin_manager.disable_plugin(1) is False
        assert plugin_manager.check_plugin_record_exists(id=1) is None
        assert plugin_manager.check_plugin_record_exists_by_id(1) is None

    def test00_not_exist_name(self, plugin_manager) :
        assert CMagPluginManager.import_plugin('a') is None
        assert CMagPluginManager.import_plugin_by_path('a') is None
        assert plugin_manager.add_plugin('a') is None
        assert plugin_manager.get_loaded_plugin_by_callname('a') is None

    def test00_db_not_exist_id(self, plugin_manager) :
        plugin_manager.add_plugin('cmag.builtin.hello')
        assert plugin_manager.get_plugin_record_by_id(1).id == 1
        with pytest.raises(Exception) as CMagPluginModelDoesNotExist : #list index out of range
            assert plugin_manager.get_plugin_record_by_id(2).id is None 

    def test00_options(self, plugin_manager) :
        plugin_manager.add_plugin('cmag.builtin.hello')
        plugin_manager.set_plugin_options(1, 'a')
        assert plugin_manager.get_plugin_options(1) == 'a'

    def test00_doubly_enable(self, plugin_manager) :
        plugin_manager.add_plugin('cmag.builtin.hello')
        plugin_manager.enable_plugin(1)
        plugin_manager.enable_plugin(1)
        assert plugin_manager.get_plugin_record(CMagPluginModel.enabled==True).id == 1

    def test00_doubly_disable(slef, plugin_manager) :
        plugin_manager.add_plugin('cmag.builtin.hello')
        plugin_manager.disable_plugin(1)
        plugin_manager.disable_plugin(1)
        assert plugin_manager.get_plugin_record(CMagPluginModel.enabled==False).id == 1

    def test00_doubly_add_plugin(self, plugin_manager) :
        plugin_manager.add_plugin('cmag.builtin.hello')
        plugin_manager.add_plugin('cmag.builtin.hello')
        loaded, total = plugin_manager.load_all()
        assert loaded == 1 and total == 1

    def test00_list_plugin(self, plugin_manager) :
        callname = HelloPlugin.callname
        plugin_manager.add_plugin('cmag.builtin.hello')
        for i, plugin in enumerate(plugin_manager.list_plugins(), 1) :
            assert plugin.id == i
            assert plugin.callname == callname

    def test00_doubly_load_plugin(self, plugin_manager) :
        callname = HelloPlugin.callname
        plugin_manager.add_plugin('cmag.builtin.hello')
        plugin_manager.load_plugin(1)
        plugin_manager.load_plugin(1)
        assert plugin_manager.get_loaded_plugin(1).id == 1
        assert plugin_manager.get_loaded_plugin(2) is None
        assert plugin_manager.get_loaded_plugin_by_callname(callname).callname == callname

    def test00_doubly_unload_plugin(self, plugin_manager) :
        callname = HelloPlugin.callname
        plugin_manager.load_plugin_once('cmag.builtin.hello')
        plugin_manager.load_plugin_once('cmag.builtin.hello')
        assert plugin_manager.unload_plugin_once(callname) is True
        assert plugin_manager.unload_plugin_once(callname) is True


class Test00CMagPluginOptions :
    pass #Not Implemented