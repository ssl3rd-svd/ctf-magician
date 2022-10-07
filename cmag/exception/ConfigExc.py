from .BaseExc import *

class CMagConfigException(CMagException):
    pass

class CMagConfigWarning(CMagWarning):
    pass

class CMagConfigLoadFailed(CMagConfigException):
    def __init__(self, baseexc=None, *args):
        super().__init__(self, *args)
        self.baseexc = baseexc
        
class CMagConfigSaveFailed(CMagConfigWarning):
    def __init__(self, baseexc=None, *args):
        super().__init__(self, *args)
        self.baseexc = baseexc
