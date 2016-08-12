from invoke import ctask as task
from invoke import Collection
from invoke.tasks import call

from jinn import helpers

from . import build, docs, test


@task(name='clean-python')
def clean_python(ctx):
    """Remove Python file artifacts."""
    ctx.run('find . -name \'*.pyc\' -delete')
    ctx.run('find . -name \'*.pyo\' -delete')
    ctx.run('find . -name \'*~\' -delete')
    ctx.run('find . -name \'__pycache__\' -delete')


@task(pre=[build.clean, call(docs.clean, builddir='_build'), clean_python, test.clean])
def clean(ctx):
    """Remove all build, test, coverage and Python artifacts."""
    pass


@task(name='clean-backups')
def clean_backups(ctx, force=False):
    """Remove backup files."""
    if not force:
        answer = helpers.confirmation_prompt("Do you want to remove all backup files?")
    if force or answer:
        ctx.run('find . -name \'*~\' -delete')
        ctx.run('find . -name \'*.orig\' -delete')
        ctx.run('find . -name \'*.swp\' -delete')


@task(name='clean-bundles')
def clean_bundles(ctx):
    """Remove webpack development bundles."""
    ctx.run('rm -f {ctx.pkg_name}/webpack-stats-development.json'.format(ctx=ctx))
    ctx.run('rm -fr {ctx.pkg_name}/static/bundles-development/'.format(ctx=ctx))


@task
def develop(ctx):
    """Install (or update) all packages required for development."""
    ctx.run('pip install -U pip setuptools wheel')
    ctx.run('pip install -U -e .')
    ctx.run('pip install -U -r requirements/dev.pip')


@task
def isort(ctx):
    """Run isort to correct imports order."""
    ctx.run('isort --recursive setup.py {ctx.pkg_name} tests/'.format(ctx=ctx))


ns = Collection(clean_python, clean, clean_backups, clean_bundles, develop, isort, build, docs,
    test)
jinn_config = helpers.load_config_section(('base_dir', 'default_env', 'pkg_name'))

if jinn_config.get('tasks'):
    helpers.add_tasks(ns, jinn_config.pop('tasks'))

ns.configure(helpers.INVOKE_CONFIG)
ns.configure(jinn_config)
