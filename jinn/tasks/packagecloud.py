import os
import sys

from invoke import ctask as task
from invoke import Collection

from jinn import helpers


@task
def upload(ctx):
    """Upload a release to packagecloud."""
    if not os.environ.get('PACKAGECLOUD_TOKEN'):
        sys.stderr.write('PACKAGECLOUD_TOKEN environment variable is required!')
    else:
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
