"""Sphinx configuration."""
# pylint: disable=invalid-name

from datetime import datetime

project = "salt-gnupg-rotate"
author = "Ryan Addessi"
copyright = f"{datetime.now().year}, {author}"  # pylint: disable=redefined-builtin


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
