from jinn.tasks import standardjs


def test_check(simple_mock_context):
    files = 'mithril_extension.js latest_framework.js'
    standardjs.check(simple_mock_context, files)
    results = str(simple_mock_context.mock_calls)
    assert 'node_modules/.bin/standard' in results
    assert files in results


def test_format(simple_mock_context):
    files = 'mithril_extension.js latest_framework.js'
    standardjs.format(simple_mock_context, files)
    results = str(simple_mock_context.mock_calls)
    assert 'node_modules/.bin/standard-format -w' in results
    assert files in str(simple_mock_context.mock_calls)
