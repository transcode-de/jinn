import webbrowser

from invoke import ctask as task


@task(name="test-upload")
def test_upload(ctx):
    """Upload a release to test PyPI using twine."""
    ctx.run('twine upload -r test -s dist/*')
    webbrowser.open('https://testpypi.python.org/pypi/{ctx.pkg_name}'.format(ctx=ctx))


@task
def upload(ctx):
    """Upload a release using twine."""
    ctx.run('twine upload -s dist/*')
    webbrowser.open('https://pypi.python.org/pypi/{ctx.pkg_name}'.format(ctx=ctx))
