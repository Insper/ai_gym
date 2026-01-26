from setuptools import setup, find_packages

setup(
    name="aigyminsper",
    version="0.2.6",
    packages=['aigyminsper','aigyminsper.search'],
    install_requires=[
        "graphviz ==0.21",
        "matplotlib ==3.10.6",
        "networkx ==3.5",
        "pydot ==4.0.1",
        "pyparsing ==3.2.3",
    ],
    author='Fabricio Barth',
    author_email='fabriciojb@insper.edu.br',
    description='A libray that helps you to learn Artificial Intelligence.',
    long_description=open("ABOUT.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/insper/ai_gym/",
    license='MIT',
    data_files=[('dist', ['ABOUT.md'])]
)
