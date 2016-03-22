import pytest

from jinn.tasks import pypi


@pytest.mark.parametrize(('function', 'command'), [
    ('test_upload', 'twine upload -r test -s dist/*'),
    ('upload', 'twine upload -s dist/*')
])
def test_test_upload(function, command, mock_context, mocker):
    pkg_name = 'my-pkg'
    mock_context = mock_context('pkg_name', pkg_name)
    mocker.patch('webbrowser.open')
    getattr(pypi, function)(mock_context)
    result = str(mock_context.mock_calls)
    # pkg_name is only to open pypi in webbrowser
    assert pkg_name not in result
    assert command in result
