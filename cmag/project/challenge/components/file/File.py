class CMagFile:
    
    def __init__(self, filemanager, file_id):
        self._id = file_id
        self._filemanager = filemanager

    @property
    def id(self):
        return self._id
