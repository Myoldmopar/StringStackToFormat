import codecs
import os
from setuptools import setup, find_packages

from epformatline import VERSION

this_dir = os.path.abspath(os.path.dirname(__file__))
with codecs.open(os.path.join(this_dir, 'README.md'), encoding='utf-8') as i_file:
    long_description = i_file.read()

setup(
    name='StringStackToFormat',
    version=VERSION,
    packages=find_packages(exclude=['test', 'tests', 'test.*']),
    url='https://github.com/Myoldmopar/StringStackToFormat',
    license='',
    author='Edwin Lee',
    author_email='',
    description='A Python tool for generating format statements.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    test_suite='nose.collector',
    tests_require=['nose'],
    keywords='energyplus',
    include_package_data=True,
    install_requires=[],
    entry_points={
        'console_scripts': [
            'epformat=epformatline.main:main_embed',
            'epformatgui=epformatline.main:main_gui',
            'epformat_interactive=epformatline.main:main_cli'
        ],
    },
    python_requires='>=3.5',
)
