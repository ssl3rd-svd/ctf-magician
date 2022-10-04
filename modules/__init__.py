from .extractor import init as extractor_init
from .scanner   import init as scanner_init

def init(project):
    modules = []
    modules += extractor_init(project)
    modules += scanner_init(project)
    return modules