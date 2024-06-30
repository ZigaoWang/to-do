from setuptools import setup, find_packages

setup(
    name='todo-cli',
    version='1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'colorama',
        'click',
        'reportlab',
    ],
    entry_points='''
        [console_scripts]
        todo=todo.cli:cli
    ''',
)