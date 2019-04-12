from pathlib import Path
from shutil import rmtree
import subprocess
import sys

import twine  # noqa
import wheel  # noqa

from pyceo import __version__


HERE = Path(__file__).parent.resolve()


def call(cmd):
    return subprocess.check_call(cmd, shell=True)


def publish():
    try:
        print("Removing previous builds…")
        rmtree(str(HERE / "dist"))
    except OSError:
        pass

    call("{0} setup.py install".format(sys.executable))

    print("Building Source and Wheel distribution…")
    call("{0} setup.py sdist bdist_wheel".format(sys.executable))

    print("Uploading the package to PyPI…")
    call("twine upload dist/*")

    print("Pushing git tags…")
    call("git tag v{0}".format(__version__))
    call("git push --tags")


if __name__ == "__main__":
    publish()
