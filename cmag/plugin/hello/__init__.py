from cmag.plugin        import CMagPlugin
from cmag.plugin.option import plugin_options

@plugin_options
class HelloPluginOptions:
    hello:str = ''
    world:str = '!'

class HelloPlugin(CMagPlugin):
    
    callname = 'cmag.plugin.hello'
    optdef = HelloPluginOptions

    def run(self, *args, **kwargs):
        print(f"Hello CTF-Magician{self.options.world}")
        print(f"hello: {self.options}")
