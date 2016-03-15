from jinn.tasks import build


def test_clean(mock_context):
    build.clean(mock_context)
    assert str(mock_context.mock_calls).count('rm -fr') == 3


def test_dist(mock_context):
    build.dist(mock_context)
    assert 'python setup.py sdist bdist_wheel' in str(mock_context.mock_calls)
    assert 'ls -l dist' in str(mock_context.mock_calls)
