from jinn.tasks import django
import pytest


def test_clean_static_root(mock_context):
    pkg_name = 'my-pkg'
    mock_context = mock_context('pkg_name', pkg_name)
    django.clean_static_root(mock_context)
    result = str(mock_context.mock_calls)
    assert result.count(pkg_name) == 2
    assert result.count('static_root') == 2
    assert 'git checkout --' in result


def test_fixtures(mock_context):
    default_env = 'prod'
    mock_context = mock_context('default_env', default_env)
    django.fixtures(mock_context)
    result = str(mock_context.mock_calls)
    assert default_env in result
    assert 'loaddata sites.json' in result
    assert 'loadtestdata users.User:10' in result


def test_manage(mock_context):
    default_env = 'prod'
    command = 'diffsettings'
    context = mock_context('default_env', default_env)
    django.manage(context, command)
    result = str(context.mock_calls)
    assert default_env in result
    assert command in result
    context = mock_context('default_env', default_env)
    django.manage(context, command, 'dev')
    result = str(context.mock_calls)
    assert default_env not in result
    assert command in result


def test_runserver(mock_context):
    pass


@pytest.mark.parametrize('command', [
    'migrate',
    'shell'
])
def test_shell(command, mock_context):
    default_env = 'prod'
    mock_context = mock_context('default_env', default_env)
    getattr(django, command)(mock_context)
    result = str(mock_context.mock_calls)
    assert default_env in result
    assert command in result