from .scanner import ArchiveFilesScanner
from .cpio import init as cpio_init
from .tar  import init as tar_init
from .zip  import init as zip_init

def init(project):
    mods = [ArchiveFilesScanner(project)]
    mods += cpio_init(project)
    mods += tar_init(project)
    mods += zip_init(project)
    return mods