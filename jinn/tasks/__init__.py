import os

from invoke import ctask as task
from invoke import Collection
from invoke.tasks import call

from . import build, db, django, docs, helpers, packagecloud, pypi, standardjs, test


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
    """Remove webpack bundle artifacts."""
    ctx.run('rm -f {pkg_name}/webpack-stats-development.json'.format(pkg_name=ctx.pkg_name))
    ctx.run('rm -fr {pkg_name}/static/bundles-development/'.format(pkg_name=ctx.pkg_name))


@task
def develop(ctx):
    """Install (or update) all packages required for development."""
    ctx.run('pip install -U pip setuptools wheel')
    ctx.run('pip install -U -e .')
    ctx.run('pip install -U -r requirements/dev.txt')


@task
def isort(ctx):
    """Run isort to correct imports order."""
    command = 'isort --recursive setup.py {pkg_name}/ tasks/ tests/'.format(pkg_name=ctx.pkg_name)
    ctx.run(command)


ns = Collection(clean_python, clean, clean_backups, clean_bundles, develop, build, db, django,
    docs, isort, packagecloud, pypi, standardjs, test)
ns.configure({
    'base_dir': os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'env': 'dev',
    'pkg_name': 'myproject',
    'run': {
        'echo': True,
        'pty': True,
    },
})
