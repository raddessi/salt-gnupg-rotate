"""Sphinx configuration."""
# ruff: noqa: INP001

from datetime import datetime, timezone

project = "salt-gnupg-rotate"
author = "Ryan Addessi"
copyright = f"{datetime.now(tz=timezone.utc).year}, {author}"  # noqa: A001


autodoc_typehints = "description"
autosectionlabel_maxdepth = 1
copybutton_prompt_text = r">>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: "
copybutton_prompt_is_regexp = True
copybutton_only_copy_prompt_lines = True
exclude_patterns = [
    "spelling_wordlist.txt",
    "_build",
]
extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "sphinx_copybutton",
    "sphinx_inline_tabs",
    "sphinxcontrib.mermaid",
    "sphinxcontrib.spelling",
    "sphinxemoji.sphinxemoji",
    "sphinx_multiversion",
]
templates_path = [
    "_templates",
]
html_theme = "furo"
myst_enable_extensions = [
    "colon_fence",
]
myst_heading_anchors = 1
source_suffix = {
    ".rst": "restructuredtext",
    ".txt": "markdown",
    ".md": "markdown",
}
spelling_show_suggestions = True
spelling_word_list_filename = ["spelling_wordlist.txt"]
spelling_exclude_patterns = ["changelog.md"]
smv_branch_whitelist = r"^main$"  # do not whitelist any branches
smv_remote_whitelist = r"^origin$"
smv_tag_whitelist = r"^v\d+\.\d+\.\d+$"
