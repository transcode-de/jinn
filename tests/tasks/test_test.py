from jinn.tasks import test


def test_all(simple_mock_context):
    test.all(simple_mock_context)
    assert 'tox' in str(simple_mock_context.mock_calls)


def test_clean(simple_mock_context):
    test.clean(simple_mock_context)
    result = str(simple_mock_context.mock_calls)
    assert result.count('rm -fr') == 3
    assert 'coverage' in result


def test_coverage(simple_mock_context):
    test.coverage(simple_mock_context)
    result = str(simple_mock_context.mock_calls)
    assert 'coverage report' in result


def test_coverage_html(simple_mock_context, mocker):
    mocker.patch('webbrowser.open')
    test.coverage_html(simple_mock_context)
    result = str(simple_mock_context.mock_calls)
    assert 'coverage html' in result


def test_run(simple_mock_context):
    test_args = '-k test_run'
    env = 'test'
    test.run(simple_mock_context)
    result = str(simple_mock_context.mock_calls)
    assert test_args not in result
    test.run(simple_mock_context, test_args, env)
    result = str(simple_mock_context.mock_calls)
    assert test_args in result
    assert env in result
