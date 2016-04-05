import os

from invoke import ctask as task
from invoke import Collection

from jinn import exceptions, helpers


@task
def upload(ctx):
    """Upload a release to packagecloud."""
    try:
        os.environ['PACKAGECLOUD_TOKEN']
    except KeyError:
        raise exceptions.EnvironmentVariableRequired('PACKAGECLOUD_TOKEN')
    repository = '{ctx.packagecloud.username}/{ctx.pkg_name}/{distro}'.format(
        ctx=ctx,
        distro='python',
    )
    for pkg in os.listdir('dist'):
        ctx.run('bundle exec package_cloud push {repository} dist/{pkg}'.format(
            repository=repository,
            pkg=pkg
        ))


ns = Collection(upload)
ns.configure(helpers.load_config_section(('username',), helpers.module_name(__file__)))
