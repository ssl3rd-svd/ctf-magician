from .ManagerExc import *

class CMagChallIDExists(CMagManagerException):
    def __init__(self, id, *args, **kwargs):
        CMagManagerException.__init__(self, *args, **kwargs)
        self.id = id

class CMagChallIDNotFound(CMagManagerException):
    def __init__(self, id, *args, **kwargs):
        CMagManagerException.__init__(self, *args, **kwargs)
        self.id = id