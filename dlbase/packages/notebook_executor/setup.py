from setuptools import setup

setup(
    name='notebook_executor',
    version='0.2',
    install_requires=['requests', 'papermill'],
    packages=['notebook_executor'],
    entry_points={
      'console_scripts': ['nbexecutor=notebook_executor.cli:main']
    }
)
