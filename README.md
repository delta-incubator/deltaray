deltaray
========

[![License](https://img.shields.io/badge/license-Apache%202-brightgreen.svg)](https://raw.githubusercontent.com/delta-incubator/deltaray/main/LICENSE)

The deltaray library provides a [Delta Lake](https://delta.io/) table reader for the [Ray](https://www.ray.io/) open-source ML toolkit.

Quickstart
----------

Install from PyPI:

    pip install deltaray

Install from GitHub:

    pip install git+https://github.com/delta-incubator/deltaray.git

Basic use, check notebooks for more detailed example:

    # Standard Libraries
    import pathlib
    
    # External Libraries
    import deltaray
    import deltalake as dl
    import pandas as pd


    # Creating a Delta Table
    cwd = pathlib.Path().resolve()
    table_uri = f'{cwd}/tmp/delta-table'
    df = pd.DataFrame({'id': [0, 1, 2, 3, 4, ], })
    dl.write_deltalake(table_uri, df)

    # Reading our Delta Table
    ds = deltaray.read_delta(table_uri)
    ds.show()

Running Test Matrix
-------------------

note: you can add -s flag to print to stderr/stdout during pytest-ing

    tox
    
Building Distribution
---------------------

Building Wheel:

    python setup.py bdist_wheel sdist

Installing Wheel:

    pip install /path/to/wheel/..
