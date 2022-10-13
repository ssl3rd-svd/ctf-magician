from cmag.plugin        import CMagPlugin
from cmag.plugin.option import plugin_options

@plugin_options
class HelloPluginOptions:
    hello:str = ''
    world:str = '!'

class HelloPlugin(CMagPlugin):
    
    callname = 'SampleHello'
    optdef = HelloPluginOptions

    def run(self, *args, **kwargs):
        self.log.info(f"Hello CTF-Magician{self.options.world}")
        self.log.warn(f"hello: {self.options}")
