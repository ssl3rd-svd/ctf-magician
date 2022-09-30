class CMagFileImpl:

    def __init__(self, path, chal):
        self._path = path
        self._chal = chal

    def scan(self):
        pass

    @property
    def chal(self):
        return self._chal

    @property
    def path(self):
        return self._path
