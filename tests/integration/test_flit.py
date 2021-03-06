from pathlib import Path

import pytest

from toxn.config import ToxConfig


@pytest.mark.network
@pytest.mark.venv
@pytest.mark.asyncio_process_pool
async def test_flit_build_and_run(project):
    proj = project({
        'pyproject.toml': f'''
[build-system]
requires = ["flit"]
build-backend = "flit.buildapi"

[tool.flit.metadata]
module = "py_mod"
author = "Happy Harry"
author-email = "happy@harry.com"
home-page = "https://github.com/happy-harry/is"

[tool.toxn]
default_tasks = ['py']
commands = ["pip list --format=columns",
            "python -c 'from py_mod import main; print(main())'"]

[tool.toxn.task.build]
python="python"
        ''',
        Path('py_mod') / '__init__.py': f'''
            """demo project"""
            __version__ = '1.0.0'
            def main():
                print("test")
        '''})
    result = await proj.run()
    assert result == 0
    conf: ToxConfig = proj.conf_obj

    assert conf.build.site_packages_dir
    assert conf.build.envbindir
    assert conf.build.python_exec
    assert conf.build.envdir
