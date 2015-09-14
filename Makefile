clean-test:
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr html/
	rm -rf cover/
	python setup.py install

test: clean-test
	nosetests --verbosity=2 -w tests

coverage: clean-test
	coverage run --source=src/dataset_creator setup.py test
	coverage report -m
	coverage html

release:
	python setup.py sdist bdist_wheel upload
