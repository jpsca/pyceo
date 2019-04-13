from pathlib import Path
from shutil import rmtree
import subprocess


HERE = Path(__file__).parent.resolve()


def call(cmd):
    return subprocess.check_output(cmd, shell=True)


def publish():
    import twine  # noqa
    import wheel  # noqa

    try:
        print("Removing previous builds…")
        rmtree(str(HERE / "dist"))
    except OSError:
        pass

    print("Building Source and Wheel distribution…")
    call("python setup.py sdist bdist_wheel")

    print("Uploading the package to PyPI…")
    call("twine upload dist/*")

    print("Pushing git tags…")
    version = call("python setup.py --version").strip()
    call("git tag v{}".format(version))
    call("git push --tags")


if __name__ == "__main__":
    publish()
