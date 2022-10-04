from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    from typing import Any, Dict, List

from pathlib import Path

class CMagProjConfFieldBase:

    name = ''
    init = None
    required = False

    OP_NONE = 0
    OP_INIT = 1
    OP_SAVE = 2

    def get(config, op, key=''):
        raise NotImplementedError
    def set(config, op, key='', value=None):
        raise NotImplementedError

class CMagProjConfFieldDefault(CMagProjConfFieldBase):
    
    init=None

    def get(config, op, key=''):
        if key in config.data:
            return config.data[key]

    def set(config, op, key='', value=init):
        config.data[key] = value

class CMagProjConfFieldAbsolutePath(CMagProjConfFieldBase):

    init: Path = None

    def get(config, op, key='', *args, **kwargs):
        if key in config.data:
            if op == CMagProjConfFieldBase.OP_NONE:
                return Path(config.data[key]).absolute()
            elif op == CMagProjConfFieldBase.OP_SAVE:
                return str(Path(config.data[key]).absolute())
            else:
                raise NotImplementedError

    def set(config, op, key='', value=[], *args, **kwargs):
        config.data[key] = Path(value).absolute()

class CMagProjConfFieldAbsolutePathList(CMagProjConfFieldBase):

    init: List[Path] = []

    def get(config, op, key='', *args, **kwargs):
        if key in config.data:
            if op == CMagProjConfFieldBase.OP_NONE:
                return [Path(p).absolute() for p in config.data[key]]
            elif op == CMagProjConfFieldBase.OP_SAVE:
                return [str(Path(p).absolute()) for p in config.data[key]]
            else:
                raise NotImplementedError

    def set(config, op, key='', value=[], *args, **kwargs):
        config.data[key] = [Path(p).absolute() for p in value]

class fieldtypes:
    base = CMagProjConfFieldBase
    default = CMagProjConfFieldDefault
    abspath = CMagProjConfFieldAbsolutePath
    abspathlist = CMagProjConfFieldAbsolutePathList