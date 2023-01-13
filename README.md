deltaray
========

Delta reader for the Ray open-source toolkit for building ML applications

Quickstart
----------

Install remotely from GitHub:

    pip install git+https://github.com/delta-incubator/deltaray.git --upgrade

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
