import os
import webbrowser

from invoke import ctask as task
from invoke import Collection

from jinn import helpers


@task
def all(ctx):
    """Run unit tests on every Python version with tox."""
    ctx.run('tox')


@task
def clean(ctx):
    """Remove test and coverage artifacts."""
    ctx.run('rm -fr .cache/')
    ctx.run('rm -fr .tox/')
    ctx.run('coverage erase')
    ctx.run('rm -fr htmlcov/')


@task
def coverage(ctx, env=None):
    """Generate a coverage report with the default Python."""
    ctx.run(helpers.envdir(ctx, 'coverage run -m pytest tests/', env or ctx.default_env))
    ctx.run('coverage report')


@task(pre=[coverage], name='coverage-html')
def coverage_html(ctx):
    """Generate and open a HTML coverage report with the default Python and open it in the default browser."""
    uri = 'file://{cwd}/htmlcov/index.html'.format(cwd=os.getcwd())
    ctx.run('coverage html')
    webbrowser.open(uri)


@task
def run(ctx, test_args='', env=None):
    """Run unit tests quickly with the default Python."""
    command = 'py.test {test_args} tests/'.format(test_args=test_args)
    ctx.run(helpers.envdir(ctx, command, env or ctx.default_env))


ns = Collection(all, clean, coverage, coverage_html, run)
