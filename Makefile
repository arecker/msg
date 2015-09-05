SETUP = python setup.py
INSTALL = pip install --force-reinstall

all:
	${SETUP} clean
	${SETUP} build
clean:
	${SETUP} clean
test:
	tox
install:
	${INSTALL} ./
