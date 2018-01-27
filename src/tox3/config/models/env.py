import argparse
import re
import shlex
from pathlib import Path
from typing import Dict, List, Optional, cast

from toxn.venv import VEnv
from .core import CommonToxConfig
from ..project import ConfDict


class EnvConfig(CommonToxConfig):

    def __init__(self,
                 _options: argparse.Namespace,
                 config_dict: ConfDict,
                 work_dir: Path,
                 name: str) -> None:
        self._work_dir = work_dir / name
        self.name = name
        # generated by running
        self.venv: Optional[VEnv] = None  # virtualenv generation

        super().__init__(_options, config_dict)

    @property
    def work_dir(self) -> Path:
        return self._work_dir

    def _extract_command(self, commands: List[str]) -> List[List[str]]:
        result = []
        for command in commands:
            command = self._substitute(command).strip().replace('\n', '\\n')
            cmd = shlex.split(command)
            if cmd:
                result.append([c.replace('\\n', '\n') for c in cmd])
        return result

    @property
    def python(self) -> str:
        key = self._config_dict.get('python')
        if key is None:
            return self.resolve_python_key(self.name)
        return cast(str, key)

    @staticmethod
    def resolve_python_key(key: str) -> str:
        match = re.match(r'py(\d?)(\d*)', key)
        if match:
            major = match.group(1)
            minor = match.group(2)
            return 'python{}{}'.format(major, '' if not minor else f'.{minor}')
        return 'python'  # fallback to the default python

    @property
    def recreate(self) -> bool:
        return cast(bool, getattr(self._cli, 'recreate', False))

    @property
    def envsitepackagesdir(self) -> Path:
        self.ensure_venv_ready()
        return cast(VEnv, self.venv).params.site_package

    @property
    def envbindir(self) -> Path:
        self.ensure_venv_ready()
        return cast(VEnv, self.venv).params.bin_path

    def ensure_venv_ready(self) -> None:
        if self.venv is None:
            raise TypeError('virtual environment not yet created')

    @property
    def envdir(self) -> Path:
        self.ensure_venv_ready()
        return cast(VEnv, self.venv).params.root_dir

    @property
    def envpython(self) -> Path:
        self.ensure_venv_ready()
        return cast(VEnv, self.venv).params.executable

    @property
    def envname(self) -> str:
        return self.name

    @property
    def install_command(self) -> List[str]:
        cmd = self._config_dict.get('install_command')
        if cmd is None:
            return ['pip', 'install', '-U']
        return shlex.split(cmd)

    @property
    def set_env(self) -> Dict[str, str]:
        result: Dict[str, str] = {}
        for key, value in self._config_dict.get('set_env', {}).items():
            result[key] = self._substitute(value)
        return result

    @property
    def pass_env(self) -> List[str]:
        return self._config_dict.get('pass_env', [])
