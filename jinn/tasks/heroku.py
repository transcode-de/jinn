import os, sys

from invoke import ctask as task
from invoke import Collection


#pre=[dist]
@task(name='compile-requirements')
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
            ctx.run('heroku pg:backups capture DATABASE_URL --app mysite-staging')
            ctx.run('bin/deploy --app mysite-staging --version $$(git describe --tags)')
            heroku_run(ctx, app='mysite-staging', command='site-admin check --deploy')
            heroku_run(ctx, app='mysite-staging', command='site-admin migrate')
            heroku_run(ctx, app='mysite-staging', command='site-admin raven test')

@task
def promote(ctx, app):
    ctx.run('heroku pg:backups capture DATABASE_URL --app mysite-production')
    ctx.run('heroku pipelines:promote --app mysite-staging')
    heroku_run(ctx, app='mysite-production', command='site-admin check --deploy')
    heroku_run(ctx, app='mysite-production', command='site-admin migrate')
    heroku_run(ctx, app='mysite-production', command='site-admin raven test')
    """Promote the staging release to production on Heroku."""


def heroku_run(ctx, app, command):
    """Helper to wrap command with heroku run."""
    ctx.run('heroku run --app {app} --exit-code {command}'.format(
        app=app,
        comand=comand
    ))


ns = Collection(deploy, promote)
ns.configure({
    'heroku': {
        'staging-app-postfix': 'staging',
        'production-app-postfix': 'production',
    },
})
