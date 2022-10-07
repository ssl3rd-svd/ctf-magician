from cmag.config import CMagConfig

class CMagProjectConfig(CMagConfig):
    defaults = {
        'name': 'ctf-magician project',
        'description': 'This is ctf-magician project.',
        'plugins': [
            'cmag.plugin.feeder',
            'cmag.plugin.scanner',
        ],
        'challenges': [],
    }
