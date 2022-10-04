from .base import CMagCmdHandlerBase as handler

class CMagCmdProjectHandler(handler):
    ''' yooyoyoyo '''

    name = 'project'
    usage = ''
    description = 'hey, this is description'

    def create_parser(self, parser):
        parser.add_argument("-a")
        parser.add_argument("-b")

    def handle(self, *args, **kwargs):
        print(self)
        print(args)
        print(kwargs)