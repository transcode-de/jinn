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


@pytest.mark.parametrize(('command', 'output'), [
    ('drop', 'dropdb -e -U'),
    ('drop_user', 'dropuser -e'),
])
def test_drop(mock_context, command, output):
    context = mock_context(db)
    getattr(db, command)(context, force=True)
    result = str(context.run.mock_calls)
    assert output in result
