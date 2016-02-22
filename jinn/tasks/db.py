from invoke import ctask as task
from invoke import Collection

from . import helpers


@task
def create(ctx, env=None):
    """Create a new PostgreSQL database."""
    command = ''.join((
        'createdb -U {username} -l en_US.utf-8 -E utf-8 -O {username}',
        ' -T template0 -e {database}'
    ))
    command = command.format(database=ctx.db.database, username=ctx.db.username)
    ctx.run(helpers.envdir(ctx, command, env or ctx.env))


@task(name='create-user')
def create_user(ctx, env=None):
    """Create a new PostgreSQL user."""
    ctx.run(helpers.envdir(ctx, 'createuser -d -e {username}'.format(
        username=ctx.db.username), env or ctx.env,
    ))


@task
def drop(ctx, env=None, force=False):
    """Drop database."""
    command = 'dropdb -e -U {username} {database}'.format(
        database=ctx.db.database,
        username=ctx.db.username
    )
    msg = "Database \"{database}\" will be permanently removed.\nAre you sure?".format(
        database=ctx.db.database
    )
    if not force:
        answer = helpers.confirmation_prompt(msg)
    if force or answer:
        ctx.run(helpers.envdir(ctx, command, env or ctx.env))


@task(name='drop-user')
def drop_user(ctx, env=None, force=False):
    """Drop database user."""
    command = 'dropuser -e {username}'.format(username=ctx.db.username)
    msg = "Role \"{username}\" will be permanently removed.\nAre you sure?".format(
        username=ctx.db.username
    )
    if not force:
        answer = helpers.confirmation_prompt(msg)
    if force or answer:
        ctx.run(helpers.envdir(ctx, command, env or ctx.env))


ns = Collection(create, create_user, drop, drop_user)
ns.configure({
    'db': {
        'database': 'my-project',
        'username': 'my-project',
        'password': 'my-project',
    },
})
