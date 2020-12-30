.ONESHELL:
SHELL := /bin/bash
SRC = $(wildcard ./*.ipynb)

all: nb_cdk docs

nb_cdk: $(SRC)
	nbdev_build_lib
	touch nb_cdk

sync:
	nbdev_update_lib

docs_serve: docs
	cd docs && bundle exec jekyll serve

docs: $(SRC)
	nbdev_build_docs
	touch docs

test:
	nbdev_test_nbs

release: pypi
	nbdev_conda_package
	nbdev_bump_version

pypi: dist
	twine upload --repository pypi dist/*

dist: clean
	python setup.py sdist bdist_wheel

clean:
	rm -rf dist