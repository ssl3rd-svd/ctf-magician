from .initial import init as init

def init(project):
    modules = []
    modules += init(project)
    return modules