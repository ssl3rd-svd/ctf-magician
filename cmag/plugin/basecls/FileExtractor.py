from .FilePluginBase import CMagFilePluginBase as file_plugin

class CMagFileExtractor(file_plugin):

    target='*'

    def check(self, path: str, *args, **kwargs):
        raise NotImplementedError

    def run(self, chall_id: str, file_id: int, *args, **kwargs):
        raise NotImplementedError