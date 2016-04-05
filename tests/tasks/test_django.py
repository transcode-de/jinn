import pytest

from jinn.tasks import django


def test_clean_static_root(mock_context):
    context = mock_context(django)
    django.clean_static_root(context)
    result = str(context.run.mock_calls)
    assert result.count(context.pkg_name) == 2
    assert result.count('static_root') == 2
    assert 'git checkout --' in result


def test_fixtures(mock_context):
    context = mock_context(django)
    django.fixtures(context)
    result = str(context.run.mock_calls)
    assert 'loaddata sites.json' in result
    assert 'loadtestdata users.User:10' in result


def test_manage(mock_context):
    command = 'diffsettings'
    context = mock_context(django)
    django.manage(context, command)
    result = str(context.run.mock_calls)
    assert command in result


def test_runserver(mock_context):
    port = 8080
    context = mock_context(django)
    django.runserver(context)
    result = str(context.run.mock_calls)
    assert context.django.port in result
    assert 'runserver' in result
    django.runserver(context, port)
    result = str(context.run.mock_calls)
    assert context.django.port in result
    assert 'runserver' in result


@pytest.mark.parametrize('command', [
    'migrate',
    'shell',
])
def test_migrate_shell(command, mock_context):
    context = mock_context(django)
    getattr(django, command)(context)
    result = str(context.run.mock_calls)
    assert command in result


def test_start_app(mock_context, mocker):
    app_name = 'jinn'
    context = mock_context(django)
    mocker.patch('os.mkdir')
    django.startapp(context, app_name)
    result = str(context.run.mock_calls)
    assert app_name in result
    assert 'apps' in result
