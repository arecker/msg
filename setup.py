from pip.req import parse_requirements
from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md')) as f:
    long_description = f.read()
install_reqs = parse_requirements(
    path.join(here, 'requirements', 'prod.txt'), session=False)
test_reqs = parse_requirements(
    path.join(here, 'requirements', 'test.txt'), session=False)

setup(
    name='msg',
    version='1.0.0',
    description='Like salt, but a little tastier',
    long_description=long_description,
    url='https://github.com/arecker/msg',
    author='Alex Recker <alex@reckerfamily.com>',
    license='GPLv3',
    packages=['msg', ],
    entry_points={
        'console_scripts': [
            'msg=msg.cli:main',
        ],
    },
    install_requires=[str(ir.req) for ir in install_reqs],
    tests_require=[str(ir.req) for ir in test_reqs],
    test_suite='nose.collector',
)
