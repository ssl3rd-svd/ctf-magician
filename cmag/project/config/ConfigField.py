from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    from typing import Any, Dict, List

from pathlib import Path

class CMagConfFieldBase:

    name = ''
    desc = ''
    init = None
    required = False
    null = True

    OP_NONE = 0
    OP_INIT = 1
    OP_SAVE = 2

    def get(config, op, key=''):
        raise NotImplementedError
    def set(config, op, key='', value=None):
        raise NotImplementedError

class CMagProjConfFieldString(CMagConfFieldBase):
    
    init=''

    def get(config, op, key=''):
        if key in config.data:
            return str(config.data[key])

    def set(config, op, key='', value=init):
        config.data[key] = str(value)

class CMagProjConfFieldInteger(CMagConfFieldBase):
    
    init=0

    def get(config, op, key=''):
        if key in config.data:
            return int(config.data[key])

    def set(config, op, key='', value=init):
        if type(value) == int:
            config.data[key] = value
        elif type(value) == str:
            if value.startswith('0x'):
                config.data[key] = int(value, 16)
            else:
                config.data[key] = int(value)
        else:
            raise TypeError

class CMagProjConfFieldAbsolutePath(CMagConfFieldBase):

    init: Path = ''

    def get(config, op, key='', *args, **kwargs):
        if key in config.data:
            if op == CMagConfFieldBase.OP_NONE:
                return Path(config.data[key]).absolute()
            elif op == CMagConfFieldBase.OP_SAVE:
                return str(Path(config.data[key]).absolute())
            else:
                raise NotImplementedError

    def set(config, op, key='', value='', *args, **kwargs):
        print(f'{key}:{value}')
        config.data[key] = Path(value).absolute()

class CMagProjConfFieldAbsolutePathList(CMagConfFieldBase):

    init: List[Path] = []

    def get(config, op, key='', *args, **kwargs):
        if key in config.data:
            if op == CMagConfFieldBase.OP_NONE:
                return [Path(p).absolute() for p in config.data[key]]
            elif op == CMagConfFieldBase.OP_SAVE:
                return [str(Path(p).absolute()) for p in config.data[key]]
            else:
                raise NotImplementedError

    def set(config, op, key='', value=[], *args, **kwargs):
        config.data[key] = [Path(p).absolute() for p in value]

class CMagFieldTypes:
    base = CMagConfFieldBase
    string = CMagProjConfFieldString
    integer = CMagProjConfFieldInteger
    abspath = CMagProjConfFieldAbsolutePath
    abspathlist = CMagProjConfFieldAbsolutePathList