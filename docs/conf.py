# https://www.sphinx-doc.org/en/master/usage/configuration.html
"""Configuration file for the Sphinx documentation builder."""

from __future__ import annotations

import os
from pathlib import Path
from runpy import run_path

from sphinx.application import Sphinx
from sphinx.util import logging

logger = logging.getLogger(__name__)

PROJECT_ROOT_DIR = Path(__file__).parents[1].resolve()
IS_RELEASE_ON_RTD = (
    os.getenv("READTHEDOCS", "False") == "True"
    and os.environ["READTHEDOCS_VERSION_TYPE"] == "tag"
)


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
    "sphinxcontrib.towncrier.ext",  # provides `.. towncrier-draft-entries::`
    "sphinx_issues",
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

issues_github_path = "aio-libs/aiofastnet"

towncrier_draft_autoversion_mode = "draft"
towncrier_draft_include_empty = True
towncrier_draft_working_directory = PROJECT_ROOT_DIR
towncrier_draft_config_path = "towncrier.toml"  # relative to towncrier_draft_working_directory

nitpicky = True

suppress_warnings = [
    # MyST erroneously flags the draft changelog as having improper header levels
    # because it starts at H2 instead of H1.
    # However, it is written only for inclusion in a broader doc, so the heading
    # levels are actually correct.
    "myst.header",
]

# -- myst_parser options --------------------------------------------------
myst_enable_extensions = {
    "colon_fence",
}


# -- Sphinx extension-API `setup()` hook


def setup(app: Sphinx) -> dict[str, bool | str]:
    """Register project-local Sphinx extension-API customizations.

    :param app: Initialized Sphinx app instance.
    :returns: Extension metadata.
    """
    if IS_RELEASE_ON_RTD:
        app.tags.add("is_release")

    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
        "version": release,
    }
