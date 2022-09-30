import os
import json
import copy
import shutil

from cmag.utils import *
from cmag.manager.file import CMagFileImpl

class CMagChallengeImpl:

    def __init__(self, chaldir, project):

        self._project = project

        # Load directory info
        self._dirname = os.path.dirname(chaldir)
        self._dir = chaldir
        self._makepath = makepath_factory(chaldir)

        # Load info
        self._info = {}
        if not os.path.isfile(self.info_file_path):
            raise Exception

        with open(self.info_file_path, 'r') as f:
            self._info = json.loads(f.read())

        # Load files
        self._files = []
        if not os.path.isdir(self.makepath('/files')):
            raise Exception

        for file in self.info['files']:
            filepath = self.makepath(f'/files/{file}')
            if not os.path.isfile(filepath):
                raise Exception
            fileobj = CMagFileImpl(self, filepath)
            self._files.append(fileobj)

    def __del__(self):
        self.save()

    def save(self):
        with open(self.info_file_path, 'w') as f:
            f.write(json.dumps(self.info))

    def add_file(self, path):
        raise NotImplementedError

    def del_file(self, path):
        raise NotImplementedError

    def scan(self):
        self._scan_queries = []
        while self._scan_queries:
            query   = self._scan_queries.pop(0)
            scanner = query['scanner']
            args    = query['args']
            kwargs  = query['kwargs']
            scanner(*args, **kwargs)

    def scan_add(self, query):
        self._scan_queries.append(copy.deepcopy(query))

    def scan_all(self):
        
        self.scan_add({
            'scanner' : CMagChallengeImpl.scan_chal,
            'args'    : (self,),
            'kwargs'  : {}
        })

        self.scan_add({
            'scanner' : CMagChallengeImpl.scan_files,
            'args'    : (self,),
            'kwargs'  : {'files': self.files}
        })

    def scan_chal(self):
        pass

    def scan_files(self, files=[]):
        pass

    def makepath(self, *args):
        return self._makepath

    @property
    def name(self): return self.info['name']

    @property
    def project(self): return self._project

    @property
    def dir(self): return self._dir

    @property
    def dirname(self): return self._dirname

    @property
    def info_file_path(self): return os.path.join(self.dir, 'info.json')

    @property
    def info(self): return self._info

    @property
    def files(self): return self._files


class CMagChallenge:
    
    CATEGORIES = {
        'pwn'   : 1,
        'rev'   : 2,
        'misc'  : 3,
        ''      : None
    }

    def new(chaldir, project, name, category, files=[], desc=''):

        makepath = makepath_factory(chaldir)

        ini, val = CMagChallenge.guess_category(category)
        if not ini or not val:
            raise Exception
        else:
            category = val

        for file in files:
            if not os.path.isfile(file):
                raise Exception

        os.makedirs(makepath('/'))
        os.makedirs(makepath('/files'))

        _files = []
        for file in files:
            filename = os.path.basename(file)
            copyto = makepath(f'/files/{filename}')
            shutil.copyfile(file, copyto)
            _files.append(filename)

        with open('info.json', 'w') as f:
            f.write(json.dumps({
                'name': name,
                'category': category,
                'files': _files,
                'desc': desc
            }))

        return CMagChallengeImpl(chaldir, project)

    def load(chaldir, project):
        return CMagChallengeImpl(chaldir, project)

    def guess_category(category):
        category = category.lower()
        for ini, val in CMagChallenge.CATEGORIES:
            if category.startswith(ini):
                return ini, val

    def get_category_by_initial(initial):
        return CMagChallenge.CATEGORIES[initial]

    def get_category_by_enumval(enumval):
        for ini, val in CMagChallenge.CATEGORIES:
            if val == enumval:
                return ini