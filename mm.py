#!/usr/bin/env python
"""
COPY THIS FILE TO YOUR PROJECT.
---------
This file generates all the necessary files for packaging for the project.
Read more about it at https://github.com/jpscaletti/mastermold/
"""
from pathlib import Path


data = {
    "title": "pyceo",
    "name": "pyceo",
    "pypi_name": "pyceo",
    "version": "2.1.0",
    "author": "Juan-Pablo Scaletti",
    "author_email": "juanpablo@jpscaletti.com",
    "description": "A minimal and ridiculously good looking command-line-interface toolkit.",
    "copyright": "2013",
    "repo_name": "jpscaletti/pyceo",
    "home_url": "",
    "project_urls": {
    },
    "development_status": "5 - Production/Stable",
    "minimal_python": 3.6,
    "install_requires": [
        "colorama ~= 0.4.1",
    ],
    "testing_requires": [
        "pytest",
    ],
    "development_requires": [
        "tox",
        "flake8",
    ],
    "entry_points": "copier = copier.cli:run",

    "coverage_omit": [
    ],

    "has_docs": False,
    "google_analytics": "UA-XXXXXXXX-X",
    "docs_nav": [],
}

exclude = [
    "copier.yml",
    "README.md",
    ".git",
    ".git/*",
    ".venv",
    ".venv/*",

    "CONTRIBUTING.md",
    "docs",
    "docs/*",
]


def do_the_thing():
    import copier
    from ruamel.yaml import YAML

    def save_current_nav():
        yaml = YAML()
        mkdocs_path = Path("docs") / "mkdocs.yml"
        if not mkdocs_path.exists():
            return
        mkdocs = yaml.load(mkdocs_path)
        data["docs_nav"] = mkdocs.get("nav")

    if data["has_docs"]:
        save_current_nav()

    copier.copy(
        # "gh:jpscaletti/mastermold.git",
        "../mastermold",  # Path to the local copy of Master Mold
        ".",
        data=data,
        exclude=exclude,
        force=True,
        cleanup_on_error=False
    )


if __name__ == "__main__":
    do_the_thing()
