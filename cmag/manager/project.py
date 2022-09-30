import json
import os
import sys
import hashlib
import time
import shutil
import importlib.util

from cmag.utils import *
from cmag.manager.challenge import CMagChallenge

class CMagProjectImpl:
    
    def __init__(self, projdir):
        
        # Load directory informations.
        self._dirname   = os.path.dirname(projdir)
        self._dir       = projdir
        self._makepath  = makepath_factory(projdir)

        # Load configurations.
        config_path = self.makepath('/config.json')
        if not os.path.isfile(config_path):
            raise Exception

        with open(config_path, 'r') as f:
            self._config = json.loads(f.read())

        # Load challenges
        chals_path = self.makepath('/chals/info.json')
        if not os.path.isfile(chals_path):
            raise Exception

        with open(chals_path, 'r') as f:
            chals = json.loads(f.read())

        self._chals = []
        for dirname in chals:

            chaldir = self.makepath(f'/chals/{dirname}')
            if not os.path.isdir(chaldir):
                raise Exception

            chalobj = CMagChallenge.load(chaldir, self)
            self._chals.append(chalobj)

        # Load modules
        self._modules = []
        for name, path in self.config['modules'].itmes():
            spec = importlib.util.spec_from_file_location(name, path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            if hasattr(module, 'init'):
                self._modules.extend(module.init(self))

    def __del__(self):
        self.save()

    def save(self):
        
        # Save configurations
        config_path = self.makepath('/config.json')
        with open(config_path, 'w') as f:
            f.write(json.dumps(self.config))
        
        # Save challenges
        chals = []
        for chal in self.chals:
            chal.save()
            chals.append(chal.dirname)

        chals_path = self.makepath('/chals/info.json')
        with open(chals_path, 'w') as f:
            f.write(json.dumps(chals))

    def add_chal(self, name, category, files=[]):

        dirname = hashlib.md5(f"{name}.{time.time()}".encode()).hexdigest()

        chaldir = self.makepath(f'/chals/{dirname}')
        if os.path.isdir(chaldir):
            raise FileExistsError(f"wtf? {chaldir} exists.")

        if self.get_chal_by_name(name):
            return Exception

        chalobj = CMagChallenge.new(chaldir, self, name, category, files)
        self._chals.append(chalobj)

    def del_chal(self, name):
        for chal in self.chals:
            if chal.name == name:
                shutil.rmtree(chal.dir)
                self._chals.pop(chal)
                break

    def get_chal_by_name(self, name):
        for chal in self.chals:
            if chal.name == name:
                return chal

    def makepath(self, *args, **kwargs):
        return self._makepath(*args, **kwargs)

    @property
    def dir(self):
        return self._dir

    @property
    def config(self):
        return self._config

    @property
    def chals(self):
        return self._chals

    @property
    def modules(self):
        return self._modules

class CMagProject:

    def new(projdir, config):

        if os.path.isdir(projdir):
            raise FileExistsError(f"Directory {projdir} already exists.")

        makepath = makepath_factory(projdir)

        os.makedirs(makepath('/'))
        os.makedirs(makepath('/challs'))

        with open(makepath('/config.json'), 'w') as f:
            f.write(json.dumps(config))
        
        return CMagProjectImpl(projdir)

    def load(projdir):
        if not os.path.isdir(projdir):
            raise FileNotFoundError(f"Directory {projdir} not found.")
        else:
            return CMagProjectImpl(projdir)
