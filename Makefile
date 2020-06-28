clean-test:
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr html/
	rm -rf cover/

test: clean-test
	nosetests --verbosity=2 --with-coverage --cover-package dataset_creator -w tests

coverage: test
	coverage report -m --include=dataset_creator/*
	coverage html

release:
	python setup.py sdist bdist_wheel upload
