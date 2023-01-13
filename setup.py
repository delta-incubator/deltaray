from setuptools import setup, find_namespace_packages


APP_NAME = "deltaray"
VERSION = "0.0.0"
LICENSE = "Apache License"
AUTHOR = "James Hibbard"
DESCRIPTION = (
    "Delta reader for the Ray open-source toolkit for building ML applications"
)

setup(
    name=APP_NAME,
    version=VERSION,
    license=LICENSE,
    author=AUTHOR,
    description=DESCRIPTION,
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
