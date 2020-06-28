clean-test:
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr html/
	rm -rf cover/

test: clean-test
	nosetests --verbosity=2 --with-coverage -w tests

coverage: test
	coverage report -m
	coverage html

release:
	python setup.py sdist bdist_wheel upload
