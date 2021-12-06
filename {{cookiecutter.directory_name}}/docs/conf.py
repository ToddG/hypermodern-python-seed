"""Sphinx configuration."""
import os
import sys

sys.path.insert(0, os.path.abspath("../src"))

project = "{{cookiecutter.project_name}}"
author = "{{cookiecutter.author_name}}"
copyright = f"2020, {author}"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.graphviz",
    "sphinx_autodoc_typehints",
]