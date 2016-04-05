from unittest.mock import MagicMock

import pytest

from jinn import exceptions
from jinn.tasks import packagecloud


def test_upload(mock_context, mocker, monkeypatch):
    dist_files = ['script.py, holidays.png']
    context = mock_context(packagecloud)
    with pytest.raises(exceptions.EnvironmentVariableRequired) as exception_info:
        packagecloud.upload(context)
    assert 'PACKAGECLOUD_TOKEN' in str(exception_info.value)
    monkeypatch.setenv('PACKAGECLOUD_TOKEN', 'my secret token')
    mocker.patch('os.listdir', MagicMock(return_value=dist_files))
    packagecloud.upload(context)
    result = str(context.run.mock_calls)
    assert result.count('bundle exec package_cloud push') == len(dist_files)
    for file in dist_files:
        assert file in result
