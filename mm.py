#!/usr/bin/env python
"""
COPY THIS FILE TO YOUR PROJECT.
---------
This file generates all the necessary files for packaging for the project.
Read more about it at https://github.com/jpscaletti/mastermold/
"""
data = {
    "title": "pyceo",
    "name": "pyceo",
    "pypi_name": "pyceo",
    "version": "2.191002",
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
        "pytest-cov",
    ],
    "entry_points": "copier = copier.cli:run",

    "coverage_omit": [
    ]
}

exclude = [
    "copier.yml",
    "README.md",
    ".git",
    ".git/*",
    ".venv",
    ".venv/*",

    "CHANGELOG.md",
    "CONTRIBUTING.md",
]


def do_the_thing():
    import copier

    copier.copy(
        # "gh:jpscaletti/mastermold.git",
        "../mastermold",  # Path to the local copy of Master Mold
        ".",
        data=data,
        exclude=exclude,
        force=False,
        cleanup_on_error=False
    )


if __name__ == "__main__":
    do_the_thing()
