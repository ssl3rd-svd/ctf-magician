from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    from typing import Any, Dict, List, Optional, Tuple

import sys
from io import IOBase
from termcolor import colored

from logging import (
    Logger, StreamHandler, FileHandler, Formatter,
    getLogger,
    DEBUG, INFO, WARN, WARNING, ERROR, CRITICAL
)

class CMagStreamFormatter(Formatter):

    dbg_fmt  = f"[{colored('D', color='white',  attrs=['bold'])}] %(msg)s"
    info_fmt = f"[{colored('i', color='cyan',   attrs=['bold'])}] %(msg)s"
    warn_fmt = f"[{colored('!', color='yellow', attrs=['bold'])}] %(msg)s"
    err_fmt  = f"[{colored('-', color='red',    attrs=['bold'])}] %(msg)s"
    crit_fmt = f"{colored(' CRITICAL ', color='red', attrs=['bold', 'reverse'])} %(msg)s"

    def __init__(self):
        super().__init__(fmt="%(levelno)d: %(msg)s", datefmt=None, style='%')  
    
    def format(self, record):

        format_orig = self._style._fmt

        if record.levelno == DEBUG:
            self._style._fmt = CMagStreamFormatter.dbg_fmt
        elif record.levelno == INFO:
            self._style._fmt = CMagStreamFormatter.info_fmt
        elif record.levelno == WARN:
            self._style._fmt = CMagStreamFormatter.warn_fmt
        elif record.levelno == ERROR:
            self._style._fmt = CMagStreamFormatter.err_fmt
        elif record.levelno == CRITICAL:
            self._style._fmt = CMagStreamFormatter.crit_fmt
        else:
            raise Exception

        result = Formatter.format(self, record)

        self._style._fmt = format_orig

        return result

class CMagLogger:

    name    = "ctf-magician"
    DEBUG   = DEBUG
    INFO    = INFO
    WARN    = WARN
    WARNING = WARNING
    ERROR   = ERROR
    CRITIAL = CRITICAL

    def __init__(self, root: str = '',
                       logger: Logger = None,
                       log_level: int = INFO,
                       log_to_stream: Optional[IOBase] = sys.stderr,
                       stream_log_level: int = INFO,
                       stream_formatter: Formatter = CMagStreamFormatter(),
                       log_to_file: Optional[str] = None,
                       file_log_level: int = DEBUG,
                       file_formatter: Formatter = None):
        
        if not logger:
            self._log = getLogger(self.name)
        else:
            self._log = logger

        self.log.setLevel(log_level)

        if (stream := log_to_stream):
            handler = StreamHandler(stream)
            handler.setLevel(stream_log_level)
            if stream_formatter:
                handler.setFormatter(stream_formatter)
            self.log.addHandler(handler)

        if (filepath := log_to_file):
            handler = FileHandler(filepath)
            handler.setLevel(file_log_level)
            if file_formatter:
                handler.setFormatter(file_formatter)
            self.log.addHandler(handler)

    @property
    def log(self) -> Logger:
        return self._log

    def create_logger(self, logger_name: str = '') -> Logger:
        logger = getLogger(self.name + '.' + logger_name)
        # logger.setLevel(self.log.level)
        # for handler in self.log.handlers:
        #     logger.addHandler(handler)
        return logger
