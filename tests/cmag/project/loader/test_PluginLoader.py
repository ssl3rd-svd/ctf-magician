import pytest

from shutil import copyfile
from pathlib import Path

from cmag.project.loader import CMagPluginLoader
from cmag.plugin.basecls import CMagInitialScanner, CMagChallengeScanner, CMagFileScanner, CMagFileExtractor

@pytest.fixture
def plugin_file_path(tmp_path):
    copysrc = Path(__file__).parent / 'sample_plugin.py'
    copydst = tmp_path / 'sample_plugin.py'
    copyfile(copysrc, copydst)
    return copydst

@pytest.fixture
def plugin_dir_path(tmp_path):
    copysrc = Path(__file__).parent / 'sample_plugin.py'
    copydst_dir = tmp_path / 'sample_plugin'
    copydst_dir.mkdir()
    copydst = copydst_dir / '__init__.py'
    copyfile(copysrc, copydst)
    return copydst_dir

@pytest.fixture
def wrong_plugin_file_path(tmp_path):
    copysrc = Path(__file__).parent / 'sample_plugin_wrong.py'
    copydst = tmp_path / 'wrong_plugin.py'
    copyfile(copysrc, copydst)
    return copydst

@pytest.fixture
def wrong_plugin_dir_path(tmp_path):
    copysrc = Path(__file__).parent / 'sample_plugin_wrong.py'
    copydst_dir = tmp_path / 'wrong_plugin'
    copydst_dir.mkdir()
    copydst = copydst_dir / '__init__.py'
    copyfile(copysrc, copydst)
    return copydst_dir

class Test0CMagPluginLoader:

    def test0_load_by_path(self, plugin_file_path, plugin_dir_path, wrong_plugin_file_path, wrong_plugin_dir_path):

        # correct

        loader = CMagPluginLoader(None, plugins_path=[str(plugin_file_path)])
        assert loader.all
        loader = CMagPluginLoader(None, plugins_path=[str(plugin_dir_path)])
        assert loader.all
        loader = CMagPluginLoader(None, plugins_path=[str(plugin_file_path), str(plugin_dir_path)])
        assert len(loader.all) == 8

        # wrong

        try:
            loader = CMagPluginLoader(None, plugins_path=[str(wrong_plugin_file_path)])
            loader = CMagPluginLoader(None, plugins_path=[str(wrong_plugin_dir_path)])
            loader = CMagPluginLoader(None, plugins_path=[str(wrong_plugin_file_path), str(wrong_plugin_dir_path)])
        except Exception:
            pass

    def test0_load_by_name(self, plugin_file_path, plugin_dir_path):

        import sys

        sys.path.append(plugin_file_path.parent)
        loader = CMagPluginLoader(None, plugins_name=[str(plugin_file_path.stem)])
        assert loader.all

        sys.path.append(plugin_dir_path.parent)
        loader = CMagPluginLoader(None, plugins_name=[str(plugin_dir_path.name)])
        assert loader.all

    def test1_get_plugins_of(self, plugin_file_path):

        loader = CMagPluginLoader(None, plugins_path=[str(plugin_file_path)])
        
        assert loader.initial_scanners
        assert isinstance(loader.initial_scanners[0], CMagInitialScanner)

        assert loader.challenge_scanners
        assert isinstance(loader.challenge_scanners[0], CMagChallengeScanner)

        assert loader.file_scanners
        assert isinstance(loader.file_scanners[0], CMagFileScanner)

        assert loader.file_extractors
        assert isinstance(loader.file_extractors[0], CMagFileExtractor)

    def test2_find_plugin_by_name(self, plugin_file_path):

        loader = CMagPluginLoader(None, plugins_path=[str(plugin_file_path)])

        assert loader.find_plugin_by_name('sample.initial')
        assert loader.find_plugin_by_name('sample.challenge')
        assert loader.find_plugin_by_name('sample.file.scanner')
        assert loader.find_plugin_by_name('sample.file.extractor')