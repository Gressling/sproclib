# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

# Add the process_control package to Python path
sys.path.insert(0, os.path.abspath('../../'))
sys.path.insert(0, os.path.abspath('../../../'))

# Mock external dependencies that aren't available during documentation build
from unittest.mock import MagicMock

class Mock(MagicMock):
    @classmethod
    def __getattr__(cls, name):
        return MagicMock()

MOCK_MODULES = [
    'numpy', 'scipy', 'matplotlib', 'matplotlib.pyplot', 'pandas',
    'cvxpy', 'pyomo', 'control', 'jupyter'
]
sys.modules.update((mod_name, Mock()) for mod_name in MOCK_MODULES)

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'SPROCLIB - Semantic Process Control Library'
copyright = '2024, Thorsten Gressling'
author = 'Thorsten Gressling'
release = '1.0.0'

# The full version, including alpha/beta/rc tags
version = '1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary', 
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'sphinx.ext.mathjax',
    # 'sphinx_autodoc_typehints',  # Disabled due to mock conflicts
    # 'myst_parser'  # Temporarily disabled to resolve parser issues
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

# Suppress import warnings during doc build
autodoc_mock_imports = [
    'numpy', 'scipy', 'matplotlib', 'pandas', 'cvxpy', 'pyomo', 'control', 'jupyter'
]

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
    'canonical_url': '',
    'analytics_id': '',
    'logo_only': False,
    'display_version': True,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': False,
    'vcs_pageview_mode': '',
    'style_nav_header_background': '#2980B9',
    # Toc options
    'collapse_navigation': True,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False
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
html_title = 'SPROCLIB - The TensorFlow/Keras for Chemical Engineering'
html_short_title = 'SPROCLIB Semantic API'

# Custom sidebar
html_sidebars = {
    '**': [
        'about.html',
        'navigation.html',
        'relations.html',
        'searchbox.html',
        'donate.html',
    ]
}

# Custom CSS for semantic theme
html_css_files = [
    'custom.css',
]

# Add JavaScript for interactive examples
html_js_files = [
    'semantic_examples.js',
]

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

# Suppress warnings for now during development
suppress_warnings = [
    'image.nonlocal_uri',
    'toc.not_readable',
    'autodoc.import_object',
    'ref.option'
]

# Don't show warnings as errors during development
nitpicky = False
