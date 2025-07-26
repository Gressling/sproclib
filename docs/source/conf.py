# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

# Add the process_control package to Python path
sys.path.insert(0, os.path.abspath('../../'))
sys.path.insert(0, os.path.abspath('../../../'))

# Add these autodoc settings
autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'show-inheritance': True,
    'special-members': '__init__',
}

# Mock external dependencies that aren't available during documentation build
import sys
from unittest.mock import MagicMock

class Mock(MagicMock):
    @classmethod
    def __getattr__(cls, name):
        return MagicMock()

# Comprehensive mock for all external dependencies
MOCK_MODULES = [
    'numpy', 'np', 'scipy', 'scipy.optimize', 'scipy.integrate', 'scipy.linalg',
    'matplotlib', 'matplotlib.pyplot', 'plt', 'pandas', 'pd',
    'cvxpy', 'pyomo', 'pyomo.environ', 'control', 'jupyter',
    'IPython', 'ipywidgets', 'plotly', 'bokeh', 'seaborn'
]

for mod_name in MOCK_MODULES:
    sys.modules[mod_name] = Mock()

# Also add to autodoc_mock_imports for additional safety
autodoc_mock_imports = MOCK_MODULES

# Avoid documenting private methods that cause issues
autodoc_member_order = 'bysource'
autodoc_typehints = 'description'

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'SPROCLIB - Standard Process Control Library'
copyright = '2025, Thorsten Gressling - MIT License'
author = 'Thorsten Gressling'
release = '3.0.0'

# The full version, including alpha/beta/rc tags
version = '3.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary', 
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'sphinx.ext.mathjax',
    'sphinx.ext.todo',
]

templates_path = ['_templates']
exclude_patterns = []

# Autodoc settings
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    'exclude-members': '__weakref__',
    'show-inheritance': True
}

autosummary_generate = True
autosummary_generate_overwrite = True
# autodoc_typehints = 'description'  # Disabled due to extension conflicts
# autodoc_typehints_format = 'short'

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False

# Intersphinx mapping
intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'numpy': ('https://numpy.org/doc/stable/', None),
    'scipy': ('https://docs.scipy.org/doc/scipy/', None),
    'matplotlib': ('https://matplotlib.org/stable/', None),
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

html_theme_options = {
    "source_repository": "https://github.com/paramus/sproclib/",
    "source_branch": "main",
    "source_directory": "docs/source/",
    "sidebar_hide_name": False,
    "navigation_with_keys": True,
    "top_of_page_button": "edit",
    "announcement": None,
    "light_css_variables": {
        "color-brand-primary": "#2980B9",
        "color-brand-content": "#2980B9",
    },
    "dark_css_variables": {
        "color-brand-primary": "#4FC3F7",
        "color-brand-content": "#4FC3F7",
    },
}

# Add semantic plant design as primary content
html_context = {
    'display_github': True,
    'github_user': 'paramus',
    'github_repo': 'sproclib',
    'github_version': 'main',
    'conf_py_path': '/docs/source/',
    'semantic_api': True,  # Flag for semantic API features
}

# Add custom configuration for semantic plant design
html_title = 'SPROCLIB - Standard Chemical Process Control Library'
html_short_title = 'SPROCLIB Chemical Process Control Library'

# Custom sidebar - simplified
# html_sidebars = {
#     '**': [
#         'about.html',
#         'navigation.html', 
#         'relations.html',
#         'searchbox.html',
#         'donate.html',
#     ]
# }

# Custom CSS and JS - conditional loading
html_css_files = []
html_js_files = []

# Only load custom files if they exist (avoid Read the Docs errors)
import os
static_path = os.path.join(os.path.dirname(__file__), '_static')
if os.path.exists(os.path.join(static_path, 'custom.css')):
    html_css_files.append('custom.css')
if os.path.exists(os.path.join(static_path, 'semantic_examples.js')):
    html_js_files.append('semantic_examples.js')

# Master document (starting page)
master_doc = 'index'

# Source file suffixes and parser configuration
source_suffix = {
    '.rst': None,
}

# Remove .md files from source_suffix if MyST is causing issues
# myst_enable_extensions = [
#     "colon_fence",
#     "deflist", 
#     "html_admonition",
#     "html_image",
#     "linkify",
#     "replacements",
#     "smartquotes",
#     "substitution",
#     "tasklist",
# ]

# MyST parser heading anchors
# myst_heading_anchors = 3

# Add todo extension for development
todo_include_todos = True

# Suppress warnings for cleaner build
suppress_warnings = [
    'image.nonlocal_uri',
    'toc.not_readable',
    'autodoc.import_object',
    'ref.option',
    'ref.python',
    'misc.highlighting_failure',
    'toc.excluded',
    'autodoc'
]

# Don't show warnings as errors during development
nitpicky = False
nitpick_ignore = [
    ('py:class', 'optional'),
    ('py:class', 'array-like'),
    ('py:class', 'callable'),
    ('py:class', 'dict-like'),
]
