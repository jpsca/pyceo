from pathlib import Path
from shutil import rmtree
import os
import sys

import twine  # noqa

from pyceo import __version__


HERE = Path(__file__).parent.resolve()


def run():
    try:
        print("Removing previous builds…")
        rmtree(str(HERE / "dist"))
    except OSError:
        pass

    print("Building Source and Wheel (universal) distribution…")
    os.system("{0} setup.py sdist bdist_wheel --universal\n".format(sys.executable))

    print("Uploading the package to PyPI via Twine…")
    os.system("twine upload dist/*")

    print("Pushing git tags…")
    os.system("git tag v{0}".format(__version__))
    os.system("git push --tags")


if __name__ == "__main__":
    run()
