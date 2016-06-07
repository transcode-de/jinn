from unittest.mock import MagicMock

import pytest

from jinn.tasks import db


@pytest.mark.parametrize(('command', 'output'), [
    ('create', 'createdb -U'),
    ('create_user', 'createuser -d -e'),
])
def test_create(mock_context, command, output):
    context = mock_context(db)
    db.create(context)
    getattr(db, command)(context)
    result = str(context.run.mock_calls)
    assert output in result


@pytest.mark.parametrize('force', [
    True,
    False,
])
@pytest.mark.parametrize(('command', 'output'), [
    ('drop', 'dropdb -e -U'),
    ('drop_user', 'dropuser -e'),
])
def test_drop(mocker, mock_context, command, output, force):
    mocker.patch('builtins.input', MagicMock(return_value='y'))
    context = mock_context(db)
    getattr(db, command)(context, force=force)
    result = str(context.run.mock_calls)
    assert output in result
