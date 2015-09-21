clean-test:
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr html/
	rm -rf cover/

test: clean-test
	nosetests --verbosity=2 -w tests

coverage: clean-test
	coverage run --source=dataset_creator setup.py test
	coverage report -m
	coverage html

release:
	python setup.py sdist bdist_wheel upload
