# base of challenge module
class ChallFailed(Exception):
    def __str__(self) -> str:
        return f'ChallFailed'

# class of challenge_impl.py
class CMagChallImplFailed(ChallFailed):
    def __str__(self) -> str:
        return f'CMagChallImplFailed'

# class of challenge.py
class CMagChallFailed(CMagChallImplFailed):
    def __str__(self) -> str:
        return f'CMagChallFailed'

# class of manager_impl.py
class CMagChallMgrImplFailed(ChallFailed):
    def __str__(self) -> str:
        return f'CMagChallMgrImplFailed'

# class of manager.py
class CMagChallMgrFailed(CMagChallMgrImplFailed):
    def __str__(self) -> str:
        return f'CMagChallMgrFailed'

# class of model.py
class CMagChallModelFailed(ChallFailed):
    def __str__(self) -> str:
        return f'CMagChallModelFailed'

# CMagChallengeImpl class
class CMagChallImplInitError(CMagChallImplFailed): 
    def __str__(self) -> str:
        return f'CMagChallImplInitError'

class CMagChallImplRecordError(CMagChallImplFailed):
    def __str__(self) -> str:
        return f'CMagChallImplRecordError'

# CMagChallenge class
class CMagChallInitError(CMagChallFailed): ...
class CMagChallCreateError(CMagChallFailed): ...
class CMagChallAddError(CMagChallFailed): ...
class CMagChallGetError(CMagChallFailed): ...
class CMagChallGetByPathError(CMagChallFailed): ...
class CMagChallListError(CMagChallFailed): ...
class CMagChallRemoveError(CMagChallFailed): ...

# CMagChallengeManagerImpl class
class CMagChallMgrImplInitError(CMagChallMgrImplFailed): ...
class CMagChallMgrImplCreateError(CMagChallMgrImplFailed): 
    def __str__(self) -> str:
        return f'CMagChallMgrImplCreateError'
class CMagChallMgrImplGetError(CMagChallMgrImplFailed): ...
class CMagChallMgrImplGetByIdError(CMagChallMgrImplFailed): ...
class CMagChallMgrImplSelectError(CMagChallMgrImplFailed): ...

# CMagChallengeManager class
class CMagChallMgrCreateError(CMagChallMgrFailed): ...
class CMagChallMgrGetError(CMagChallMgrFailed): ...
class CMagChallMgrSelectError(CMagChallMgrFailed): ...
class CMagChallMgrDeleteError(CMagChallMgrFailed): ...

# CMagChallengeModel class
class CMagChallModelError(CMagChallModelFailed): ...

# Exception raise decorator
def raise_except_decorate(exception):
    def decorator(function):
        def wrapper(self, *args, **kwargs):
            try:
                return function(self, *args, **kwargs)
            except:
                raise exception
        return wrapper
    return decorator

# Exception handler decorator
def handle_except_decorate(handler):
    def decorator(function):
        def wrapper(self, *args, **kwargs):
            try:
                return function(self, *args, **kwargs)
            except Exception as e:
                return handler(self, e)
        return wrapper
    return decorator