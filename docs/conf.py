# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.coverage',
    'sphinx.ext.doctest',
    'sphinx.ext.extlinks',
    'sphinx.ext.ifconfig',
    'sphinx.ext.napoleon',
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
]
needs_sphinx = '1.3'

source_suffix = '.rst'
master_doc = 'index'
project = 'jinn'
year = '2016'
author = 'transcode'
copyright = '{0}, {1}'.format(year, author)
version = release = '0.1.0'

pygments_style = 'trac'
templates_path = ['_templates']
exclude_patterns = ['_build']
extlinks = {
    'issue': ('https://github.com/transcode-de/jinn/issues/%s', '#'),
    'pr': ('https://github.com/transcode-de/jinn/pull/%s', 'PR #'),
}

html_theme = 'alabaster'
html_use_smartypants = True
html_last_updated_fmt = '%b %d, %Y'
html_split_index = True
html_sidebars = {
   '**': ['searchbox.html', 'globaltoc.html', 'sourcelink.html'],
}
html_short_title = '%s-%s' % (project, version)

autodoc_default_flags = []


napoleon_use_ivar = True
napoleon_use_rtype = False
napoleon_use_param = False
