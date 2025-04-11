"""
Setup script for the Renaissance Stock Ranking System.

This makes the project installable as a package and defines entry points
for command-line scripts.
"""

from setuptools import setup, find_packages

# Read requirements from requirements.txt, filtering out comments and blanks
# Note: This is a simplified approach; a more robust one might handle different markers
# or specific version specifiers differently.
core_reqs = []
with open('requirements.txt') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#'):
            # We only add core dependencies here. Others are optional or dev.
            # Based on requirements.txt structure:
            if any(pkg in line for pkg in ['pandas', 'numpy', 'matplotlib', 'seaborn', 'openpyxl', 'xlrd']):
                 core_reqs.append(line)

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
    install_requires=core_reqs, # Use dynamically read core requirements
    extras_require={
        'bloomberg': [
            # Cannot list blpapi here, but defines the feature.
            # Users install via: pip install .[bloomberg]
            # And then separately: pip install --index-url=https://bcms.bloomberg.com/pip/simple/ blpapi
            # This key signals the optional dependency set.
        ],
        'notebook': ['jupyter', 'ipywidgets'],
        'test': ['pytest', 'pytest-cov'],
        'viz': ['plotly'], # Adding plotly as optional viz dep
        # Add other optional sets if desired (e.g., 'dev', 'docs')
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