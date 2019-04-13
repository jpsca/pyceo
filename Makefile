all: PHONY

help:
	@echo "clean - remove build/python artifacts"
	@echo "test - run tests"
	@echo "flake - check style with flake8"
	@echo "testcov - check code coverage"
	@echo "coverage - generate an HTML report of the coverage"
	@echo "install - install for development"

clean: clean-build clean-pyc

clean-build:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf pip-wheel-metadata

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -rf {} +
	find . -name '.pytest_cache' -exec rm -rf {} +
	find . -name '*.egg-info' -exec rm -rf {} +

test:
	pytest -x pyceo tests

flake:
	flake8 --config=setup.cfg pyceo tests

testcov:
	pytest --cov pyceo pyceo tests

coverage:
	pytest --cov-report html --cov pyceo pyceo tests

install:
	pip install -e .
	pip install -r requirements-dev.txt
