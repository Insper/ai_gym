from setuptools import setup, find_packages

setup(
    name="aigyminsper",
    version="0.2.4",
    packages=['aigyminsper','aigyminsper.search'],
    author='Fabricio Barth',
    author_email='fabriciojb@insper.edu.br',
    description='A libray that helps you to learn Artificial Intelligence.',
    long_description=open("ABOUT.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/insper/ai_gym/",
    license='MIT',
    data_files=[('dist', ['ABOUT.md'])]
)
