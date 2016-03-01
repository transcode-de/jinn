import os
import sys
import webbrowser

from invoke import ctask as task
from invoke import Collection


@task
def upload(ctx):
    """Upload a release to packagecloud."""
    if os.environ.get('PACKAGECLOUD_TOKEN'):
        repository = '{user}/{repo}/{distro}'.format(
            user=ctx.packagecloud.user,
            repo=ctx.pkg_name,
            distro='python',
        )
        for pkg in os.listdir('dist'):
            ctx.run('bundle exec package_cloud push {repository} dist/{pkg}'.format(
                repository=repository,
                pkg=pkg
            ))
    else:
        sys.stderr.write('PACKAGECLOUD_TOKEN environment variable is required!')


ns = Collection(upload)
ns.configure({
    'packagecloud': {
        'user': 'transcode',
    },
})
