from cmag.config import CMagConfig

class CMagChallengeConfig(CMagConfig):
    defaults = {
        'name': 'Challenge',
        'files': [],
        'urls': [],
        'sshs': [],
        'socks': [],
    }