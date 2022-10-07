from pathlib import Path

def make_dir_if_not_exists(path):
    
    dirpath = Path(path)

    if not dirpath.exists() and not dirpath.is_dir():
        dirpath.mkdir()

    return dirpath
