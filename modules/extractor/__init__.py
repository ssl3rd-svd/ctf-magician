from cmag.manager.project import CMagProjectImpl

from .zip  import ZipExtractor
from .tar  import TarExtractor
from .cpio import CPIOExtractor

def init(project: CMagProjectImpl):
    mods = []
    return mods