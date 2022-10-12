from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    from typing import Any, Dict, List
    from io import IOBase

import sys
from logging import Logger
from pathlib import Path
from cmag.database import CMagDatabase
from cmag.interface.logger import CMagLogger
from cmag.plugin.manager import CMagPluginManager
from cmag.challenge.manager import CMagChallengeManager

class CMagProjectImpl:

    def __init__(self, project_dir:str, log_level: int = CMagLogger.INFO, log_to_stream: IOBase = sys.stderr, log_to_file: str = ''):
        
        self._dir = project_dir
        self.path.mkdir(exist_ok=True)

        self._logger = CMagLogger(log_level=log_level, log_to_stream=log_to_stream, log_to_file=log_to_file)
        self._log = self.logger.log
        self.log.debug("CMagLogger initialized.")

        self._plginmgr = CMagPluginManager(self)
        self.log.debug("CMagPluginManager initialized.")

        self._challmgr = CMagChallengeManager(self)
        self.log.debug("CMagChallengeManager initialized.")

    # properties

    @property
    def dir(self):
        return self._dir

    @property
    def path(self):
        return Path(self.dir)

    @property
    def db(self):
        return CMagDatabase(self.path / 'project.db')

    # logging methods

    @property
    def logger(self) -> CMagLogger:
        return self._logger

    @property
    def log(self) -> Logger:
        return self._log

    # plugin methods

    @property
    def plugin_manager(self):
        return self._plginmgr

    # challenge methods
    
    @property
    def challenge_manager(self):
        return self._challmgr
