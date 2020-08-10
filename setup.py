from os import path
from setuptools import setup, find_packages
import sys
import versioneer


# NOTE: This file must remain Python 2 compatible for the foreseeable future,
# to ensure that we error out properly for people with outdated setuptools
# and/or pip.
if sys.version_info < (3, 6):
    error = """
fragmenter does not support Python {0}.{2}.
Python 3.6 and above is required. Check your Python version like so:

python3 --version

This may be due to an out-of-date pip. Make sure you have pip >= 9.0.1.
Upgrade pip like so:

pip install --upgrade pip
""".format(3, 6)
    sys.exit(error)

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as readme_file:
    readme = readme_file.read()

with open(path.join(here, 'requirements.txt')) as requirements_file:
    # Parse requirements.txt, ignoring any commented-out lines.
    requirements = [line for line in requirements_file.read().splitlines()
                    if not line.startswith('#')]


setup(
    name='fragmenter',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="Fragments FreeSurfer parcellation annotation' \
        ' in N-equal sized parcels.",
    long_description=readme,
    author="Michael Notter",
    author_email='michaelnotter@hotmail.com',
    url='https://github.com/miykael/parcellation_fragmenter',
    packages=find_packages(exclude=['docs', 'tests']),
    entry_points={
        'console_scripts': [
            # 'some.module:some_function',
            ],
        },
    include_package_data=True,
    package_data={
        'fragmenter': []
        },
    install_requires=requirements,
    license="BSD (3-clause)",
    classifiers=[
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
    ],
)
