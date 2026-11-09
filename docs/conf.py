# https://www.sphinx-doc.org/en/master/usage/configuration.html
"""Configuration file for the Sphinx documentation builder."""

from __future__ import annotations

from pathlib import Path
from runpy import run_path

from sphinx.util import logging

logger = logging.getLogger(__name__)

PROJECT_ROOT_DIR = Path(__file__).parents[1].resolve()


# -- Project information -----------------------------------------------------

project = "aiofastnet"
author = f"{project} Contributors"
copyright = f"The {author}"

# The full version, including alpha/beta/rc tags.
# Read the version module directly: importing the aiofastnet package would
# load its compiled extensions, which the docs environment does not build
# (tox.ini: skip_install).
release = run_path(str(PROJECT_ROOT_DIR / "aiofastnet" / "_version.py"))["__version__"]

# The short version, without any dev or local suffix
version = ".".join(release.split(".")[:3])

logger.info("%s version: %s", project, version)
logger.info("%s release: %s", project, release)

# -- General configuration ---------------------------------------------------

extensions = [
    # Third-party extensions:
    "myst_parser",
]

# Sphinx would otherwise treat every .md file in changelog.d/ (the Towncrier
# fragments and their README) as a page and fail on "not included in any
# toctree".
exclude_patterns = ["changelog.d"]

# -- Options for HTML output -------------------------------------------------

html_theme = "furo"
html_title = f"<nobr>{project}</nobr> documentation v{release}"

# The README embeds the logo as raw HTML (<img src="aiofastnet.svg">), which
# Sphinx passes through without copying the file, so copy it next to
# index.html.
html_extra_path = ["../aiofastnet.svg"]

nitpicky = True
