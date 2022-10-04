from .PluginBase import CMagPluginBase as plugin

class CMagChallengeScanner(plugin):
    def run(self, chall_id: str, *args, **kwargs):
        raise NotImplementedError