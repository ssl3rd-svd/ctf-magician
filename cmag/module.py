from cmag.manager.project import CMagProjectImpl

class ModuleBase:

    def __init__(self, project: CMagProjectImpl):
        self.project = project
        self.type    = None

    def check_file(self, chal):
        raise NotImplementedError

    def scan_file(self, fileobj):
        raise NotImplementedError

    def check_chal(self, chal):
        raise NotImplementedError

    def scan_chal(self, chalobj):        
        raise NotImplementedError
