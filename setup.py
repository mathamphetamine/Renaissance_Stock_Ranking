"""
Setup script for the Renaissance Stock Ranking System.

This makes the project installable as a package and defines entry points
for command-line scripts.
"""

from setuptools import setup, find_packages

# Define core dependencies directly
# Versions should match those previously confirmed in requirements.txt
core_reqs = [
    'pandas==2.0.3',
    'numpy==1.24.3',
    'matplotlib==3.7.2',
    'seaborn==0.12.2',
    'openpyxl==3.1.2',
    'xlrd==2.0.1',
]

# Optional dependencies defined in extras_require below

# Note: blpapi cannot be listed directly due to non-PyPI installation.
# It is handled via extras_require documentation or user action.

setup(
    name="renaissance-stock-ranking",
    version="2.0.1", # Updated version
    description="Automated Stock Ranking System", # Shortened description slightly
    long_description=open('README.md').read(), # Include README for more detail on PyPI
    long_description_content_type='text/markdown',
    author="mathamphetamine", # author
    packages=find_packages(),
    install_requires=core_reqs, # Use directly defined core requirements
    extras_require={
        # 'bloomberg' is a placeholder to signal the feature set exists.
        # Actual blpapi installation is manual (see README/docs).
        'bloomberg': [],
        'notebook': [
            'jupyter==1.0.0',  # Pinned based on previous requirements.txt
            'ipywidgets==8.0.6' # Pinned based on previous requirements.txt
        ],
        'test': [
            'pytest==7.4.0',     # Pinned based on previous requirements.txt
            'pytest-cov==4.1.0'  # Pinned based on previous requirements.txt
        ],
        'viz': [
            'plotly==5.15.0'    # Pinned based on previous requirements.txt
        ],
        # We can define a 'dev' or 'all' extra for convenience
        'dev': [
            'jupyter==1.0.0',
            'ipywidgets==8.0.6',
            'pytest==7.4.0',
            'pytest-cov==4.1.0',
            'plotly==5.15.0'
            # Add other dev tools like linters, formatters if desired
        ]
    },
    entry_points={
        'console_scripts': [
            'renaissance-rank=renaissance.cli.main:main',
            'renaissance-analyze=renaissance.cli.analyze:main',
            'renaissance-visualize=renaissance.cli.visualize:main',
            'renaissance-extract=renaissance.cli.extract:main',
        ],
    },
    python_requires='>=3.8',
    # Add classifiers, license, keywords etc. for better packaging
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License", # Update if needed
        "Operating System :: OS Independent",
        "Private :: Do Not Upload", # If not intended for PyPI
    ],
) 