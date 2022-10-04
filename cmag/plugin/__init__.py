from .feeder    import init as feeder_init
from .scanner   import init as scanner_init
from .extractor import init as extractor_init
from .fuzzer    import init as fuzzer_init

def init(project):
    return [] \
        + feeder_init(project) \
        + scanner_init(project) \
        + extractor_init(project) \
        + fuzzer_init(project)