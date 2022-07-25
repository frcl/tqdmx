import re
from distutils.core import setup


name = 'tqdmx'


def version():
    with open(f'{name}/__init__.py', 'r') as init_file:
        _version = re.search('__version__ = \'([^\']+)\'',
                             init_file.read()).group(1)
    return _version


def readme():
    with open('README.md', 'r') as readme_file:
        _readme = readme_file.read()
    return _readme


setup(
    name=name,
    version=version(),
    url='https://github.com/frcl/tqdmx',
    author='Lars Franke',
    author_email='frcl@mailbox.org',
    license='MIT',
    description='Matrix bot to interface with tqdm',
    long_description=readme(),
    long_description_content_type='text/markdown',
    packages=[name],
    install_requires=['tqdm', 'requests'],
)
