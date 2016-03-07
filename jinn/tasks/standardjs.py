from invoke import ctask as task


@task(help={'files': "files to check"})
def check(ctx, files):
    """Check javascript files for standard style."""
    standardjs_bin_path = 'node_modules/.bin/standard'
    ctx.run('{binary} {files}'.format(
        binary=standardjs_bin_path,
        files=files)
    )


@task(help={'files': "files to format"})
def format(ctx, files):
    """Format javascript files for standard style."""
    standardjs_bin_path = 'node_modules/.bin/standard-format'
    ctx.run('{binary} {arguments} {files}'.format(
        binary=standardjs_bin_path,
        arguments="-w",
        files=files)
    )
