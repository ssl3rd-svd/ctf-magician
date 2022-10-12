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