from __future__ import annotations

if __import__("typing").TYPE_CHECKING:
    from .console import CMagConsole
    from cmag.project import CMagProject
    from cmag.project.challenge import CMagChallenge

class CMagConsoleSession:
    
    def __init__(self, console_class, handler_classes):

        for handler_class in handler_classes:
            handler_obj = handler_class(self)
            setattr(console_class, 'do_' + handler_class.name, handler_obj)

        self.console: CMagConsole = console_class(self)
        self.project: CMagProject = None
        self.challenge: CMagChallenge = None
