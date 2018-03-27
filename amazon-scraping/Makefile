NAME := amazon-scraping
VERSION := 0.0.0

all: env

env:
	virtualenv env
	env/bin/pip install -r requirement.txt
	env/bin/python setup.py develop

.PHONY: test
test: env
	env/bin/py.test --verbose $(NAME)

clean:
	find . -name '*.py[oc]' -delete
	rm -rf *.egg-info
	rm -rf env


