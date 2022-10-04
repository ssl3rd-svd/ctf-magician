from secrets import token_hex

from .Challenge import CMagChallenge

class CMagChallengeManager:

    def __init__(self, project):
        self._project = project

    @property
    def project(self):
        return self._project

    @property
    def list(self):
        with self.project.database as db:
            return [CMagChallenge(self.project, challenge.id) for challenge in db.Challenge.select()]

    def get(self, id):
        with self.project.database as db:
            challenge_row = db.Challenge.get(id=id)
            if challenge_row:
                return CMagChallenge(self.project, id)

    def add(self, name, id=''):
        
        if not id:
            id = token_hex(16)

        if self.get(id):
            return self.add(name)

        with self.project.database as db:
            db.Challenge.create(id=id, name=name)

        return self.get(id)

    def remove(self, *args, **kwargs):
        pass
