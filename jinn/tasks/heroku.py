import os, sys

from invoke import ctask as task
from invoke import Collection

from . import build


@task(pre=[build.dist], name='compile-requirements')
def compile_requirements(ctx):
    """Compile the requirements for deployment."""
    ctx.run('rm -f heroku/requirements.txt')
    ctx.run('pip-compile --rebuild --find-links ./dist heroku/requirements.in')


@task
def deploy(ctx):
    """Deploy a release to Heroku."""
    if not os.environ.get('HEROKU_API_TOKEN'):
        sys.stderr.write('HEROKU_API_TOKEN environment variable is required!')
    else:
        if not os.environ.get('HEROKU_API_KEY'):
            sys.stderr.write('HEROKU_API_KEY environment variable is required!')
        else:
            app_name = '{pkg_name}-staging'.format(pkg_name=ctx.pkg_name)
            ctx.run('heroku pg:backups capture DATABASE_URL --app {app_name}'.format(
                app_name=app_name)
            )
            ctx.run('bin/deploy --app {app_name} --version $$(git describe --tags)'.format(
                app_name=app_name))
            heroku_run(ctx, app=app_name, command='site-admin check --deploy')
            heroku_run(ctx, app=app_name, command='site-admin migrate')
            heroku_run(ctx, app=app_name, command='site-admin raven test')

@task
def promote(ctx):
    """Promote the staging release to production on Heroku."""
    app_name = '{pkg_name}-production'.format(pkg_name=ctx.pkg_name)
    ctx.run('heroku pg:backups capture DATABASE_URL --app {app_name}'.format(app_name=app_name))
    ctx.run('heroku pipelines:promote --app pkg_name-staging'.format(pkg_name=ctx.pkg_name))
    heroku_run(ctx, app=app_name, command='site-admin check --deploy')
    heroku_run(ctx, app=app_name, command='site-admin migrate')
    heroku_run(ctx, app=app_name, command='site-admin raven test')


def heroku_run(ctx, app, command):
    """Helper to wrap command with heroku run."""
    ctx.run('heroku run --app {app} --exit-code {command}'.format(
        app=app,
        comand=comand
    ))
