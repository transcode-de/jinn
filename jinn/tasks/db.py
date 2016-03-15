from invoke import ctask as task
from invoke import Collection

from jinn import helpers


@task
def create(ctx, env=None):
    """Create a new PostgreSQL database."""
    command = ''.join((
        'createdb -U {ctx.db.username} -l en_US.utf-8 -E utf-8 -O {ctx.db.username}',
        ' -T template0 -e {ctx.db.database}'
    )).format(ctx=ctx)
    ctx.run(helpers.envdir(ctx, command, env or ctx.default_env))


@task(name='create-user')
def create_user(ctx, env=None):
    """Create a new PostgreSQL user."""
    ctx.run(helpers.envdir(
        ctx, 'createuser -d -e {ctx.db.username}'.format(ctx=ctx),
        env or ctx.default_env,
    ))


@task
def drop(ctx, env=None, force=False):
    """Drop the PostgreSQL database."""
    command = 'dropdb -e -U {ctx.db.username} {ctx.db.database}'.format(ctx=ctx)
    msg = "Database \"{ctx.db.database}\" will be permanently removed.\nAre you sure?".format(ctx=ctx)
    if not force:
        answer = helpers.confirmation_prompt(msg)
    if force or answer:
        ctx.run(helpers.envdir(ctx, command, env or ctx.default_env))


@task(name='drop-user')
def drop_user(ctx, env=None, force=False):
    """Drop the PostgreSQL database user."""
    command = 'dropuser -e {ctx.db.username}'.format(ctx=ctxx)
    msg = "Role \"{ctx.db.username}\" will be permanently removed.\nAre you sure?".format(ctx=ctx)
    if not force:
        answer = helpers.confirmation_prompt(msg)
    if force or answer:
        ctx.run(helpers.envdir(ctx, command, env or ctx.default_env))


ns = Collection(create, create_user, drop, drop_user)
ns.configure(helpers.load_config_section('db', ('database', 'username')))
