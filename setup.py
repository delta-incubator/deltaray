# Standard Libraries
from setuptools import setup, find_namespace_packages
import pathlib


APP_NAME = "deltaray"
VERSION = "0.1.1"
LICENSE = "Apache License"
AUTHOR = "James Hibbard"
DESCRIPTION = (
    "Delta reader for the Ray open-source toolkit for building ML applications"
)
URL = "https://github.com/delta-incubator/deltaray.git"

# Directory containing this file
HERE = pathlib.Path(__file__).parent

# Text of README.md file
README = (HERE / "README.md").read_text()

setup(
    name=APP_NAME,
    version=VERSION,
    license=LICENSE,
    author=AUTHOR,
    description=DESCRIPTION,
    long_description=README,
    long_description_content_type="text/markdown",
    url=URL,
    install_requires=[
        "deltalake>=0.6.4",
        "ray[data]>=2.2.0",
        "numpy>=1.24.1",  # typing
    ],
    extras_require={},
    packages=find_namespace_packages("src"),
    package_dir={"": "src"},
    package_data={
        "": ["*.yaml"],
    },
    entry_points="""
    [console_scripts]
    """,
    python_requires=">=3.9",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
    ],
)
