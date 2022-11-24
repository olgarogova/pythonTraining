import setuptools
from os.path import join, dirname


setuptools.setup(
    name="package-tagcounter",
    version="0.1",
    author="Olga Rogova",
    description="This is a tagcounter.",
    long_description=open(join(dirname(__file__), 'README.md'), encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    packages=['package_tagcounter'],
    entry_points={'console_scripts': ['tagcounter = package_tagcounter.tagcounter:main']},
    include_package_data=True,
    test_suite='tests'
)