"""Sphinx configuration."""
project = "{{cookiecutter.project_name}}"
author = "{{cookiecutter.author_name}}"
copyright = f"2020, {author}"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.graphviz",
    "sphinx_autodoc_typehints",
    "sphinxcontrib.mermaid",
]
