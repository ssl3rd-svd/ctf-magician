from cmag.manager import CMagProjectImpl

class CMagModuleBase:

    name=''

    def __init__(self, project: CMagProjectImpl):
        
        if self.name == '':
            raise NotImplementedError

        self.project = project

    def check(self):
        raise NotImplementedError

    def run(self):
        raise NotImplementedError

class CMagInitialScanner(CMagModuleBase):
    def run(self, chall_id: str):
        raise NotImplementedError

class CMagChallScanner(CMagModuleBase):
    def run(self, chall_id: str, *args, **kwargs):
        raise NotImplementedError

class CMagFileScanner(CMagModuleBase):

    target='*'

    def __init__(self, project: CMagProjectImpl):
        CMagModuleBase.__init__(self, project)

    def run(self, chall_id: str, file_id: int, *args, **kwargs):
        raise NotImplementedError

class CMagFileExtractor(CMagModuleBase):

    target='*'

    def __init__(self, project: CMagProjectImpl):
        CMagModuleBase.__init__(self, project)
    
    def check(self, path: str):
        pass

    def run(self, chall_id: str, file_id: int, *args, **kwargs):
        raise NotImplementedError