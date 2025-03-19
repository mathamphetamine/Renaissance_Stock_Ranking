"""
Setup script for the Renaissance Stock Ranking System.

This makes the project installable as a package and defines entry points
for command-line scripts.
"""

from setuptools import setup, find_packages

setup(
    name="renaissance-stock-ranking",
    version="1.0.0",
    description="Automated Stock Ranking System for Renaissance Investment Managers",
    author="Renaissance Investment Managers",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy",
        "matplotlib",
        "seaborn",
    ],
    entry_points={
        'console_scripts': [
            'renaissance-rank=renaissance.cli.main:main',
            'renaissance-analyze=renaissance.cli.analyze:main',
            'renaissance-visualize=renaissance.cli.visualize:main',
            'renaissance-extract=renaissance.cli.extract:main',
        ],
    },
    python_requires='>=3.8',
) 