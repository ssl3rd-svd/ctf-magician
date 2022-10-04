from .ManagerExc import *

class CMagConfigNotFound(CMagManagerException):
    def __init__(self, cfgkey: str, *args, **kwargs):
        CMagManagerException.__init__(self, *args, **kwargs)
        self.cfgkey = cfgkey
