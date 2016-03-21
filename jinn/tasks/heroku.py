import os

from invoke import ctask as task

from jinn import exceptions

from . import build


@task(pre=[build.dist], name='compile-requirements')
def compile_requirements(ctx):
    """Compile the requirements for deployment."""
    ctx.run('rm -f heroku/requirements.txt')
    ctx.run('pip-compile --rebuild --find-links ./dist heroku/requirements.in')


@task
def deploy(ctx):
    """Deploy a release to Heroku."""
    try:
        os.environ['HEROKU_API_TOKEN']
    except KeyError:
        raise exceptions.EnvironmentVariableRequired('HEROKU_API_TOKEN')
    try:
        os.environ['HEROKU_API_KEY']
    except KeyError:
        raise exceptions.EnvironmentVariableRequired('HEROKU_API_KEY')
    app_name = '{ctx.pkg_name}-staging'.format(ctx=ctx)
    ctx.run('heroku pg:backups capture DATABASE_URL --app {}'.format(app_name))
    ctx.run('bin/deploy --app {} --version $$(git describe --tags)'.format(app_name))
    heroku_run(ctx, app=app_name, command='site-admin check --deploy')
    heroku_run(ctx, app=app_name, command='site-admin migrate')
    heroku_run(ctx, app=app_name, command='site-admin raven test')


@task
def promote(ctx):
    """Promote the staging release to production on Heroku."""
    app_name = '{ctx.pkg_name}-production'.format(ctx=ctx)
    ctx.run('heroku pg:backups capture DATABASE_URL --app {}'.format(app_name))
    ctx.run('heroku pipelines:promote --app {ctx.pkg_name}-staging'.format(ctx=ctx))
    heroku_run(ctx, app=app_name, command='site-admin check --deploy')
    heroku_run(ctx, app=app_name, command='site-admin migrate')
    heroku_run(ctx, app=app_name, command='site-admin raven test')


def heroku_run(ctx, app, command):
    """Helper to wrap command with heroku run."""
    ctx.run('heroku run --app {app} --exit-code {command}'.format(
        app=app,
        command=command
    ))
