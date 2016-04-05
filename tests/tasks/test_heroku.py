import pytest

from jinn import exceptions
from jinn.tasks import heroku


def test_compile_requirements(simple_mock_context):
    heroku.compile_requirements(simple_mock_context)
    result = str(simple_mock_context.mock_calls)
    assert 'rm -f heroku/requirements.txt' in result
    assert 'pip-compile --rebuild --find-links ./dist heroku/requirements.in' in result


def test_deploy_environment_variables(mock_context, monkeypatch):
    context = mock_context()
    with pytest.raises(exceptions.EnvironmentVariableRequired) as exception_info:
        heroku.deploy(context)
    assert 'HEROKU_API_TOKEN' in str(exception_info.value)
    monkeypatch.setenv('HEROKU_API_TOKEN', 'my secret token')
    with pytest.raises(exceptions.EnvironmentVariableRequired) as exception_info:
        heroku.deploy(context)
    assert 'HEROKU_API_KEY' in str(exception_info.value)
    monkeypatch.setenv('HEROKU_API_KEY', 'my secret key')
    heroku.deploy(context)


def test_deploy(mock_context, monkeypatch):
    monkeypatch.setenv('HEROKU_API_TOKEN', 'my secret token')
    monkeypatch.setenv('HEROKU_API_KEY', 'my secret key')
    context = mock_context()
    heroku.deploy(context)
    result = str(context.run.mock_calls)
    assert 'heroku pg:backups capture DATABASE_URL --app' in result
    assert 'bin/deploy --app' in result
    assert result.count('site-admin') == 3


def test_promote(mock_context):
    context = mock_context()
    heroku.promote(context)
    result = str(context.run.mock_calls)
    assert 'heroku pg:backups capture DATABASE_URL --app' in result
    assert 'heroku pipelines:promote --app' in result
    assert result.count('site-admin') == 3


def test_heroku_run(simple_mock_context):
    app, command = 'jinn', 'site-admin check --deploy'
    heroku.heroku_run(simple_mock_context, app, command)
    result = str(simple_mock_context.mock_calls)
    assert app and command in result
