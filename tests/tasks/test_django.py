import pytest

from jinn.tasks import django


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


def test_start_app(complex_context, mocker):
    app_name = 'jinn'
    pkg_name = 'my-pkg'
    base_dir = 'base_dir'
    default_env = 'dev'

    configuration_pairs = [
        ('pkg_name', pkg_name),
        ('base_dir', base_dir),
        ('default_env', default_env)
    ]
    mock_context = complex_context(configuration_pairs)
    mocker.patch('os.mkdir')
    django.startapp(mock_context, app_name)
    result = str(mock_context.mock_calls)
    assert app_name and pkg_name and base_dir and default_env in result
    assert 'apps' in result
