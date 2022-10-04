from .InitialFilesScanner import InitialFilesScanner

def init(project):
    return [
        InitialFilesScanner(project),
    ]