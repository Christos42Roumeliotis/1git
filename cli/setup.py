from importlib.metadata import entry_points
from setuptools import setup

setup(
    name='se2128',
    version='0.1.0',
    packages=['se2128'],
    entry_points={
        'console_scripts': [
            'se2128 = se2128.__main__:main'
        ]
    }
)
