from cmd import Cmd

class CMagShell(Cmd):

    prompt = '> '

    def __init__(self, project=None, *args, **kwargs):
        Cmd.__init__(self, *args, **kwargs)
        self.project = project

    def do_exit(self, arg):
        'Exit CTF-Magician console.'
        return True