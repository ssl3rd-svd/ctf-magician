from cmag.config import CMagConfig as base

class CMagPluginConfig(base):

    defaults = {

        'type': 'manual', # initial, challenge, file, ...

        # manual-type scanner plugin's option:
        'manual.xxx': '',

        # challenge-type scanner plugin's option:
        'challenge.xxx': '',

        # file-type scanner plugin's option:
        'file.target': '*',

    }