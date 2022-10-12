# base dummy class
class DatabaseFailed(Exception):
    pass

# class of base_model.py
class CMagBaseModelFailed(DatabaseFailed):
    pass

# class of database.py
class CMagDatabaseFailed(DatabaseFailed):
    pass

class CMagBaseModelError(CMagDatabaseFailed): ...
class CMagDatabaseOpenError(CMagDatabaseFailed): ...
class CMagDatabaseCloseError(CMagDatabaseFailed): ...
class CMagDatabaseProxyError(CMagDatabaseFailed): ...