from jinn.tasks import docs


def test_clean(mock_context):
    context = mock_context(docs)
    docs.clean(context)
    result = str(context.run.mock_calls)
    assert 'make -C' and 'clean BUILDDIR=' in result


def test_html(mock_context):
    pass
