from jinn import tasks


def test_clean_python(simple_mock_context):
    tasks.clean_python(simple_mock_context)
    result = str(simple_mock_context.mock_calls)
    assert result.count('find . -name') == 4


def test_clean(simple_mock_context):
    tasks.clean(simple_mock_context)
    assert '[]' == str(simple_mock_context.mock_calls)


def test_clean_backups(simple_mock_context):
    tasks.clean_backups(simple_mock_context, force=True)
    result = str(simple_mock_context.mock_calls)
    assert result.count('find . -name') == 3


def test_clean_bundles(mock_context):
    pkg_name = 'my-pkg'
    mock_context = mock_context('pkg_name', pkg_name)
    tasks.clean_bundles(mock_context)
    result = str(mock_context.mock_calls)
    assert pkg_name in result
    assert result.count('rm -f') == 2


def test_develop(simple_mock_context):
    tasks.develop(simple_mock_context)
    result = str(simple_mock_context.mock_calls)
    assert result.count('pip install -U') == 3


def test_isort(mock_context):
    pkg_name = 'my-pkg'
    mock_context = mock_context('pkg_name', pkg_name)
    tasks.isort(mock_context)
    result = str(mock_context.mock_calls)
    assert pkg_name in result
    assert 'isort --recursive setup.py' in result
