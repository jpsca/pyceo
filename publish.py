from pathlib import Path
from shutil import rmtree
import sys

import twine  # noqa

from pyceo import __version__


HERE = Path(__file__).parent.resolve()


def run(self):
    try:
        print("Removing previous builds…")
        rmtree(str(HERE / "dist"))
    except OSError:
        pass

    print("Building Source and Wheel (universal) distribution…")
    print("{0} setup.py sdist bdist_wheel --universal\n".format(sys.executable))

    print("Uploading the package to PyPI via Twine…")
    print("twine upload dist/*")

    print("Pushing git tags…")
    print("git tag v{0}".format(__version__))
    print("git push --tags")


if __name__ == "__main__":
    run()
