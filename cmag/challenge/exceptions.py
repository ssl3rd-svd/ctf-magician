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
class ChallengeFailed(Exception):
    pass

# class of challenge_impl.py
class CMagChallengeImplFailed(ChallengeFailed):
    pass

# class of challenge.py
class CMagChallengeFailed(CMagChallengeImplFailed):
    pass

# class of manager.py
class CMagChallengeMangerFailed(ChallengeFailed):
    pass

# class of model.py
class CMagChallengeModelFailed(ChallengeFailed):
    pass

class CMagChallengeImplCreateError(CMagChallengeImplFailed): ...
class CMagChallengeImplGetError(CMagChallengeImplFailed): ...
class CMagChallengeImplSelectError(CMagChallengeImplFailed): ...
class CMagChallengeImplDeleteError(CMagChallengeImplFailed): ...

class CMagChallengeManagerCreateError(CMagChallengeMangerFailed): ...
class CMagChallengeManagerGetError(CMagChallengeMangerFailed): ...
class CMagChallengeManagerSelectError(CMagChallengeMangerFailed): ...
class CMagChallengeManagerDeleteError(CMagChallengeMangerFailed): ...

class CMagChallengeModelError(CMagChallengeModelFailed): ...