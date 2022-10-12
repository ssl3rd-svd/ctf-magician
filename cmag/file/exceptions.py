# base dummy class
class FileFailed(Exception):
    pass

# class of file.py
class CMagFileFailed(FileFailed):
    pass

# class of manager.py
class CMagFileManagerFailed(FileFailed):
    pass

# class of model.py
class CMagFileModelFailed(FileFailed):
    pass

class CMagFileError(CMagFileFailed): ...

class CMagFileManagerCreateError(CMagFileManagerFailed): ...
class CMagFileManagerGetError(CMagFileManagerFailed): ...
class CMagFileManagerSelectError(CMagFileManagerFailed): ...
class CMagFileManagerDeleteError(CMagFileManagerFailed): ...

class CMagFileModelError(CMagFileModelFailed): ...