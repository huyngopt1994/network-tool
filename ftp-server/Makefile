NAME := ftp-server
VERSION := 0.0.0

all: env update

prepare: $(NAME)/__init__.py
	echo "__version__= '${VERSION}'" > $(NAME)/__init__.py

.PHONY: check
check:
	pep8 $(NAME)
	frosted -vb -r $(NAME)

env:
	virtualenv env
	env/bin/pip install -r requirement.txt
	env/bin/python setup.py develop

.PHONY: install
install:

.PHONY: test
test: env
	env/bin/py.test --verbose $(NAME)

clean:
	find . -name '*.py[oc]' -delete
	rm -rf *.egg-info
	rm -rf env 

update:
	env/bin/python setup.py develop
