from .BaseExc import *

class CMagChallengeException(CMagException):
    pass

class CMagChallengeWarning(CMagWarning):
    pass

class CMagChallengeAddFailed(CMagChallengeException):
    def __init__(self, baseexc=None, *args):
        super().__init__(self, *args)
        self.baseexc = baseexc

class CMagChallengeOpenFailed(CMagChallengeWarning):
    pass
