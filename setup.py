from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(
    name='aigyminsper',
    version='0.1.9',
    packages=['aigyminsper','aigyminsper.search'],
    install_requires=[],
    description='A libray that helps you to learn Artificial Intelligence.',
    author='Fabricio Barth',
    author_email='fabriciojb@insper.edu.br',
    long_description=long_description,
    long_description_content_type='text/markdown',
)
