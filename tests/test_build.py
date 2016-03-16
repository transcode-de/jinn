from jinn.tasks import build


def test_clean(simple_mock_context):
    build.clean(simple_mock_context)
    assert str(simple_mock_context.mock_calls).count('rm -fr') == 3


def test_dist(simple_mock_context):
    build.dist(simple_mock_context)
    result = str(simple_mock_context.mock_calls)
    assert 'python setup.py sdist bdist_wheel' in result
    assert 'ls -l dist' in result
