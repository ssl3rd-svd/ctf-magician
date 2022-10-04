from __future__ import annotations
if __import__("typing").TYPE_CHECKING:
    from typing import Any, List, Dict
    from cmag.project import CMagProject

from .components.file import CMagFileManager

class CMagChallenge:

    def __init__(self, project: CMagProject, challenge_id: str):
        
        self._project = project
        self._id      = challenge_id
        self._files   = CMagFileManager(self)
        self._urls    = None
        self._sshs    = None
        self._sockets = None

    @property
    def project(self): return self._project

    @property
    def id(self): return self._id

    @property
    def row(self):
        with self.project.database as db:
            return db.Challenge.get(id=self.id)

    # file manager implements
    @property
    def files(self):
        return self._files

    # scan methods

    def scan(self, *args, **kwargs):
        return self.project.scan_challenge(self.id, *args, **kwargs)

    def scan_query(self, *args, **kwargs):
        return self.project.scan_query(self.id, *args, **kwargs)

    def scan_query_next(self, *args, **kwargs):
        return self.project.scan_query_next(self.id, *args, **kwargs)

    def scan_cancel_after(self, *args, **kwargs):
        return self.project.scan_cancel_after(self.id, *args, **kwargs)

    def scan_cancel_all(self, *args, **kwargs):
        return self.project.scan_cancel_all(self.id, *args, **kwargs)