import os
import webbrowser

from invoke import ctask as task
from invoke import Collection

from jinn import helpers


@task(help={'builddir': "Sphinx build directory"})
def clean(ctx, builddir=None):
    """Remove documentation artifacts."""
    command = 'make -C {path} clean BUILDDIR={builddir}'.format(
        builddir=builddir or ctx.docs.build_dir,
        path='docs'
    )
    ctx.run(command)


@task(help={'builddir': "Sphinx build directory", 'sphinxopts': "Sphinx options"})
def html(ctx, builddir=None, sphinxopts=None):
    """Build the project documentation as HTML."""
    command = 'make -C {path} html BUILDDIR={builddir} SPHINXOPTS=\'{sphinxopts}\''.format(
        builddir=builddir or ctx.docs.build_dir,
        path=ctx.docs.docs_dir,
        sphinxopts=sphinxopts or ''
    )
    ctx.run(command)


@task(help={'builddir': "Sphinx build directory"}, name='open')
def open_docs(ctx, builddir=None):
    """Open the project documentation in the default browser."""
    uri = 'file://{path}/{builddir}/html/index.html'.format(
        path=os.path.join(os.getcwd(), ctx.docs.docs_dir),
        builddir=builddir or ctx.docs.build_dir
    )
    webbrowser.open(uri)


@task(help={'builddir': "Sphinx build directory", 'port': "Port to use"})
def serve(ctx, builddir=None, port=None):
    """Serve the project documentation in the default browser."""
    webbrowser.open('http://127.0.0.1:{0}'.format(port or ctx.docs.port))
    command = 'cd docs/{builddir}/html; python -m http.server {port}'.format(
        builddir=builddir or ctx.docs.build_dir,
        port=port or ctx.docs.port
    )
    ctx.run(command)

ns = Collection(clean, html, open_docs, serve)
ns.configure(helpers.load_config_section(('build_dir', 'port'), helpers.module_name(__file__)))
