from jinn.tasks import docs


def test_clean(mock_context):
    context = mock_context(docs)
    docs.clean(context)
    result = str(context.run.mock_calls)
    assert 'make -C' and 'clean BUILDDIR=' in result


def test_html(mock_context):
    context = mock_context(docs)
    docs.html(context)
    result = str(context.run.mock_calls)
    assert 'make -C' and 'html BUILDDIR=' and 'SPHINXOPTS' in result


def test_open_docs(mock_context, mocker):
    context = mock_context(docs)
    mocker.patch('webbrowser.open')
    docs.open_docs(context)
    result = str(context.run.mock_calls)
    assert '[]' == result


def test_serve(mock_context, mocker):
    build_dir, port = 'tmp_docs', 8000
    context = mock_context(docs)
    mocker.patch('webbrowser.open')
    docs.serve(context)
    result = str(context.run.mock_calls)
    assert 'cd docs/' and 'python -m http.server' in result
    context = mock_context(docs)
    mocker.patch('webbrowser.open')
    docs.serve(context, build_dir, port)
    result = str(context.run.mock_calls)
    assert 'cd docs/' and 'python -m http.server' in result
    assert build_dir and str(port) in result
