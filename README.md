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

Running Tests
-------------

[tox](https://tox.wiki/en/latest/) standardizes running tests in Python. It handles 
creating virtual environments for running tests alongside [pytest](https://docs.pytest.org/en/latest/), our chosen testing 
library. It also handles generating reports on test results.

1. Open a bash shell (if on Windows use git bash, WSL, or any shell configured for bash commands).

2. Clone this repo and navigate to the cloned folder.

3. Install `tox` for running our test suite and managing our test environments:

    ```bash
    pip install tox
   ```

4. Run the test suite from the shell with `tox` while in the cloned repo's directory:

    ```bash
    tox -s
   ```

note: The `-s` flag prints results to stderr/stdout during pytest-ing.
    
Building Distribution
---------------------

Building Wheel:

    python setup.py bdist_wheel sdist

Installing Wheel:

    pip install /path/to/wheel/..
