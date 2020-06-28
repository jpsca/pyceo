#!/usr/bin/env python
"""
This file generates all the necessary files for packaging for the project.
Read more about it at https://github.com/jpsca/mastermold/
"""
data = {
    "title": "pyceo",
    "name": "pyceo",
    "pypi_name": "pyceo",
    "version": "2.200628",
    "author": "Juan-Pablo Scaletti",
    "author_email": "juanpablo@jpscaletti.com",
    "description": "A minimal and ridiculously good looking command-line-interface toolkit.",
    "copyright": "2013",
    "repo_name": "jpsca/pyceo",
    "home_url": "",
    "project_urls": {},
    "development_status": "5 - Production/Stable",
    "minimal_python": 3.6,
    "install_requires": [
        "colorama ~= 0.4",
    ],
    "testing_requires": [
        "pytest",
        "pytest-cov",
    ],
    "development_requires": [
        "tox",
        "flake8",
    ],
    "entry_points": "",
    "coverage_omit": []
}


def do_the_thing():
    import hecto

    hecto.copy(
        # "gh:jpsca/mastermold.git",
        "../mastermold",  # Path to the local copy of Master Mold
        ".",
        data=data,
        force=False,
        exclude=[
            ".*",
            ".*/*",
            "README.md",
        ],
    )


if __name__ == "__main__":
    do_the_thing()
