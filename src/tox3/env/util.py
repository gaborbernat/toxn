import logging
import os
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Dict, Generator, List, Tuple

from toxn.config.models.env import EnvConfig
from toxn.config.models.venv import Install
from toxn.util import Loggers


def install_params(batch_name: str, packages: List[str], config: EnvConfig,
                   develop: bool = False) -> Install:
    return Install(batch_name, packages, config.install_command, develop)


class EnvLogging(logging.LoggerAdapter):
    """
    This example adapter expects the passed in dict-like object to have a
    'connid' key, whose value in brackets is prepended to the log message.
    """

    def process(self, msg: str, kwargs: Any) -> Tuple[str, Dict[str, Any]]:
        env = self.extra.get('env')  # type: ignore
        if env is None:
            env_info = ''
        else:
            env_info = f'[{env}] '
        return f"{env_info}{msg}", kwargs


@contextmanager
def change_dir(to_dir: Path, logger: Loggers) -> Generator[None, None, None]:
    cwd = Path(os.getcwd())
    if cwd != to_dir:
        logger.debug('change cwd to %r', to_dir)
        os.chdir(str(to_dir))
    try:
        yield
    finally:
        if cwd != to_dir:
            logger.debug('change cwd to %r', to_dir)
            os.chdir(str(cwd))
