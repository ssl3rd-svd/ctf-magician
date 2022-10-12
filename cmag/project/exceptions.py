# Exception event decorator
def ExceptionDecorator(exception, handler):
    def decorator(function):
        def wrapper(self, *args, **kwargs):
            try:
                return function(self, *args, **kwargs)
            except exception as e:
                handler(self, e)
        return wrapper
    return decorator

# base dummy class
class ProjectFailed(Exception):
    pass

# class of project_impl.py
class CMagProjectImplFailed(ProjectFailed):
    pass

# class of project.py
class CMagProjectFailed(CMagProjectImplFailed):
    pass

class CMagProjectImplLoadError(CMagProjectImplFailed): ...
class CMagProjectImplUnloadError(CMagProjectImplFailed): ...
class CMagProjectImplAddError(CMagProjectImplFailed): ...
class CMagProjectImplRemoveError(CMagProjectImplFailed): ...
class CMagProjectImplGetError(CMagProjectImplFailed): ...
class CMagProjectImplEnableError(CMagProjectImplFailed): ...
class CMagProjectImplDisableError(CMagProjectImplFailed): ...
class CMagProjectImplSaveError(CMagProjectImplFailed): ...
class CMagProjectImplListError(CMagProjectImplFailed): ...
