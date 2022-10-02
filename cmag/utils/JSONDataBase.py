from json import load, dump, JSONEncoder, JSONDecoder
from pathlib import Path
from typing import Any, Dict, Tuple

class JSONDataBaseTypes:

    def __init__(self, definitions: Dict[str, Any]):

        self._definitions = definitions

        root = self

        class JSONDBEncoder(JSONEncoder):
            def encode(self, obj, *args, **kwargs):
                obj = root.check(obj, make_not_found=True)
                return JSONEncoder.encode(self, obj, *args, **kwargs)

        class JSONDBDecoder(JSONDecoder):
            def decode(self, *args, **kwargs):
                decoded = JSONDecoder.decode(self, *args, **kwargs)
                obj = root.check(decoded, raise_not_found=True)
                return obj

        self._encoder = JSONDBEncoder
        self._decoder = JSONDBDecoder

    @property
    def definitions(self): return self._definitions

    @property
    def encoder(self): return self._encoder

    @property
    def decoder(self): return self._decoder

    def check(self, obj: Dict[str, Any],
              raise_not_found=False,
              make_not_found=False,
              definitions: Dict[str, Any] = None):

        if not definitions:
            definitions = self.definitions

        new_obj = {}

        for chkkey, chktyp in definitions:

            if chkkey in obj and type(obj[chkkey]) != type(chktyp):
                raise TypeError(f"type(obj[{chkkey}]) != {type(chktyp)}")
            elif raise_not_found:
                raise KeyError(f"{chkkey} not found.")
            elif make_not_found:
                val = chktyp()
            else:
                val = obj[chkkey]

            if type(chktyp) == dict:
                val = self.check(val, raise_not_found, make_not_found, chktyp)

            if type(chktyp) == list and len(chktyp) != 0 and chktyp[0] != None:
                chktyp = chktyp[0]
                new_list = []
                if type(chktyp) == dict:
                    for v in val:
                        if type(v) != dict:
                            raise TypeError
                        v = self.check(v, raise_not_found, make_not_found, chktyp)
                        new_list.append(v)
                else:
                    for v in val:
                        if type(v) != type(chktyp):
                            raise TypeError
                        new_list.append(v)
                val = new_list

            new_obj[chkkey] = val

        return new_obj

class JSONDataBase:

    def __init__(self, filepath: str, mode: str, types: JSONDataBaseTypes):
        self._path = Path(filepath)
        self._mode = mode
        self._types = types
        self._data = {}

    def __enter__(self):
        self.load()
        return self

    def __exit__(self, type, value, traceback):
        self.save()

    def __del__(self):
        self.save()

    @property
    def path(self): return self._path

    @property
    def types(self): return self._types

    def load(self):
        if self._mode == 'w' and (self._mode == 'a' and not self._path.is_file()):
            self._data = self.types.check({}, make_not_found=True)
        else:
            with self.path.open('r') as file:
                self._data = load(file, cls=self.types.decoder)

    def save(self):
        if self._data and self._mode != 'r':
            with self.path.open('w') as file:
                dump(self._data, file, cls=self.types.encoder)

    def __getitem__(self, key: str):
        if not self.types.check_key(key):
            raise KeyError(key)
        return self._data[key]

class JSONDataBaseFactory:
    def create(definitions: Dict[str, Any]) -> Tuple[JSONDataBase, JSONDataBaseTypes]:
        types = JSONDataBaseTypes(definitions)
        class jsondb(JSONDataBase):
            def __init__(self, filepath: str, mode: str):
                JSONDataBase.__init__(self, filepath, mode, types)
        return jsondb, types
