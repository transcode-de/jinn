import pytest

from jinn.tasks import docs


@pytest.mark.xfail(reason='more complex mock_context is needed.')
def test_clean(mock_context):
    mock_context = mock_context(('docs', {'build_dir': 'build'}))
    build_dir = 'build_dir'
    docs.clean(mock_context)
    result = str(mock_context.mock_calls)
    assert '' in result
    docs.clean(mock_context)
    result = str(mock_context.mock_calls)
    assert build_dir in result
    assert 'ls -l dist' in result


def test_html(mock_context):
    pass
