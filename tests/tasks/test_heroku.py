from jinn.tasks import heroku
from jinn import exceptions
import pytest
import os


def test_compile_requirements(simple_mock_context):
    heroku.compile_requirements(simple_mock_context)
    result = str(simple_mock_context.mock_calls)
    assert 'rm -f heroku/requirements.txt' in result
    assert 'pip-compile --rebuild --find-links ./dist heroku/requirements.in' in result


def test_deploy_environment_variables(mock_context, monkeypatch):
    pkg_name = 'my-pkg'
    mock_context = mock_context('pkg_name', pkg_name)
    with pytest.raises(exceptions.EnvironmentVariableRequired) as exception_info:
        heroku.deploy(mock_context)
    assert 'HEROKU_API_TOKEN' in str(exception_info.value)
    monkeypatch.setenv('HEROKU_API_TOKEN', 'my secret token')
    with pytest.raises(exceptions.EnvironmentVariableRequired) as exception_info:
        heroku.deploy(mock_context)
    assert 'HEROKU_API_KEY' in str(exception_info.value)
    monkeypatch.setenv('HEROKU_API_KEY', 'my secret key')
    heroku.deploy(mock_context)


def test_deploy(mock_context, monkeypatch):
    monkeypatch.setenv('HEROKU_API_TOKEN', 'my secret token')
    monkeypatch.setenv('HEROKU_API_KEY', 'my secret key')
    pkg_name = 'my-pkg'
    mock_context = mock_context('pkg_name', pkg_name)
    heroku.deploy(mock_context)
    result = str(mock_context.mock_calls)
    assert pkg_name and 'staging' in result
    assert 'heroku pg:backups capture DATABASE_URL --app' in result
    assert 'bin/deploy --app' in result
    assert result.count('site-admin') == 3


def test_promote(mock_context):
    pkg_name = 'my-pkg'
    mock_context = mock_context('pkg_name', pkg_name)
    heroku.promote(mock_context)
    result = str(mock_context.mock_calls)
    assert pkg_name and 'production' in result
    assert 'heroku pg:backups capture DATABASE_URL --app' in result
    assert 'heroku pipelines:promote --app' in result
    assert result.count('site-admin') == 3


def test_heroku_run(simple_mock_context):
    app, command = 'jinn', 'site-admin check --deploy'
    heroku.heroku_run(simple_mock_context, app, command)
    result = str(simple_mock_context.mock_calls)
    assert app and command in result
