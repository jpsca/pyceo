from pathlib import Path

from setuptools import find_packages, setup


HERE = Path(__file__).parent.resolve()


setup(
    name="pyceo",
    version="2.0.2",
    description="A minimal and ridiculously good looking command-line-interface toolkit.",
    long_description=(HERE / "README.md").read_text(),
    long_description_content_type="text/markdown",
    author="Juan-Pablo Scaletti",
    author_email="juanpablo@jpscaletti.com",
    python_requires=">=3.6.0",
    url="https://github.com/jpscaletti/pyceo",
    install_requires=["colorama~=0.4.1"],
    license="MIT",
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
