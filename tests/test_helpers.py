import pytest
from invoke.collection import Collection

from jinn import exceptions, helpers


def test_envdir():
    command = 'python manage.py runserver'
    env = 'prod'
    assert env not in helpers.envdir('', command)
    assert env in helpers.envdir('', command, env)


def test_add_tasks():
    col = Collection()
    tasks = helpers.load_config_section(('tasks',)).get('tasks')
    helpers.add_tasks(col, tasks)
    for task in [task.split('.')[-1] for task in tasks.splitlines() if task]:
        assert task in col.collections.keys()


def test_load_config_section(monkeypatch):
    keys = ('database', 'username')
    env = 'JINN_CONFIG_PATH'

    monkeypatch.setenv(env, '/tmp')
    with pytest.raises(exceptions.ConfigurationFileNotFoundError):
        helpers.load_config_section(keys, 'django')

    monkeypatch.setenv(env, 'tests/tasks/broken_config')
    with pytest.raises(exceptions.ConfigurationFileSectionNotFoundError):
        helpers.load_config_section(keys, 'django')

    with pytest.raises(exceptions.ConfigurationFileSectionKeysMissingError):
        helpers.load_config_section(keys, 'db')


def test_determine_config_path(monkeypatch):
    config_path = 'tests/tasks/config'
    env = 'JINN_CONFIG_PATH'
    monkeypatch.setenv(env, config_path)
    path_from_env = helpers.determine_config_path()
    assert path_from_env.startswith(config_path)
    monkeypatch.delenv(env)
    path = helpers.determine_config_path()
    assert not path.startswith(config_path)
