.PHONY: help
help:
	@echo "clean - remove build/python artifacts"
	@echo "test - run tests"
	@echo "lint - check style with flake8"
	@echo "coverage - generate an HTML report of the coverage"
	@echo "install - install for development"

.PHONY: clean
clean: clean-build clean-pyc

.PHONY: clean-build
clean-build:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf pip-wheel-metadata
	rm -rf *.egg-info

.PHONY: clean-pyc
clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -rf {} +
	find . -name '.pytest_cache' -exec rm -rf {} +

.PHONY: test
test:
	pytest -x pyceo tests

.PHONY: lint
lint:
	flake8 --config=setup.cfg pyceo tests

.PHONY: coverage
coverage:
	pytest --cov-report html --cov pyceo pyceo tests

.PHONY: install
install:
	pip install -U pip
	pip install -e .[dev]
