from .PluginBase import CMagPluginBase as baseclass

class CMagFilePluginBase(baseclass):

    target='*'

    def check(self, path: str, *args, **kwargs):
        raise NotImplementedError

    def run(self, chall_id: str, file_id: int, *args, **kwargs):
        raise NotImplementedError