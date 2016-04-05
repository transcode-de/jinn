import pytest

from jinn.tasks import pypi


@pytest.mark.parametrize(('function', 'command'), [
    ('test_upload', 'twine upload -r test -s dist/*'),
    ('upload', 'twine upload -s dist/*')
])
def test_test_upload(function, command, mock_context, mocker):
    context = mock_context()
    mocker.patch('webbrowser.open')
    getattr(pypi, function)(context)
    result = str(context.run.mock_calls)
    assert command in result
