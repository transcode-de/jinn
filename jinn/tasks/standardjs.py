from invoke import ctask as task


@task(help={'files': "files to check"})
def check(ctx, files):
    """Check the style of all JavaScript files against JavaScript Standard Style."""
    standardjs_bin_path = 'node_modules/.bin/standard'
    ctx.run('{binary} {files}'.format(
        binary=standardjs_bin_path,
        files=files)
    )


@task(help={'files': "files to format"})
def format(ctx, files):
    """Automatically format using JavaScript Standard Style."""
    standardjs_bin_path = 'node_modules/.bin/standard-format'
    ctx.run('{binary} {arguments} {files}'.format(
        binary=standardjs_bin_path,
        arguments="-w",
        files=files)
    )
