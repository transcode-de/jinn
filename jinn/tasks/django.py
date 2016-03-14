import os

from invoke import ctask as task
from invoke import Collection

from . import helpers


@task(name='clean-static_root')
def clean_static_root(ctx):
    """Cleanup Django's STATIC_ROOT directory."""
    ctx.run('rm -fr {pkg_name}/static_root'.format(pkg_name=ctx.pkg_name))
    ctx.run('git checkout -- {pkg_name}/static_root'.format(pkg_name=ctx.pkg_name))


@task
def fixtures(ctx):
    """Load fixtures for development."""
    manage(ctx, 'loaddata sites.json')
    manage(ctx, 'loadtestdata users.User:10')


@task(help={'command': "Django command to execute", 'env': "envdir name to use"})
def manage(ctx, command, env=None):
    """Execute a Django command using the given env."""
    command = 'python {manage_py} {command}'.format(
        manage_py=os.path.join(ctx.base_dir, 'manage.py'),
        command=command
    )
    ctx.run(helpers.envdir(ctx, command, env=env or ctx.env))


@task(help={'port': "Port to use"})
def runserver(ctx, port=None):
    """Start Django's development Web server."""
    manage(ctx, 'runserver {0}'.format(port or ctx.django.port))


@task
def shell(ctx):
    """Run a Python interactive interpreter."""
    manage(ctx, 'shell')


@task
def migrate(ctx):
    """Synchronize database with current set of models and migrations."""
    manage(ctx, 'migrate')


@task(help={'name': "Name of the app to create"})
def startapp(ctx, name):
    """Create a Django app directory structure for the given app name."""
    directory = os.path.join(ctx.base_dir, ctx.pkg_name, 'apps', name)
    os.mkdir(directory)
    manage(ctx, ' '.join(('startapp', name, directory)))
    message = "".join((
        "Don't forget to add '{pkg_name}.apps.{app_name}.apps.",
        "{app_name_title}Config' to INSTALLED_APPS in '{pkg_name}.config/settings/common.py'!"
    ))
    print(message.format(
        app_name=name,
        app_name_title=name.title(),
        pkg_name=ctx.pkg_name,
    ))


ns = Collection(clean_static_root, fixtures, manage, migrate, runserver, shell, startapp)
ns.configure({
    'django': {
        'port': 8000,
    },
})
