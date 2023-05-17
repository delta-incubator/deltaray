# ![deltaray-header](./assets/deltaray-header.png)

[![License](https://img.shields.io/badge/license-Apache%202-brightgreen.svg)](https://raw.githubusercontent.com/delta-incubator/deltaray/main/LICENSE)

The deltaray library provides a [Delta Lake](https://delta.io/) table reader for the [Ray](https://www.ray.io/) open-source ML toolkit.

Quickstart
----------

Install from PyPI:

```shell
pip install deltaray
```

Install from GitHub:

```shell
pip install git+https://github.com/delta-incubator/deltaray.git
```

Basic use, check notebooks for more detailed example:

```python
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
```

Improving Read and Query Performance
------------------------------------

You can make Delta Lake queries faster by using column projection and predicate 
pushdown. These tools accelerate reads and subsequent queries by reducing the 
amount of data being sent to the Ray cluster. 

Here's an example of how to query a Delta Table with Ray and take advantage of 
column pruning and predicate pushdown filters:

```python
# Standard Libraries
from pathlib import Path

# External Libraries
import deltaray
import deltalake as dl
import pyarrow.compute as pc
import pandas as pd


# Create a Delta Table
cwd = Path.cwd()
table_uri = f'{cwd}/delta-table'
df = pd.DataFrame({
    'id': [0, 1, 2, ], 
    'name': ['Bill', 'Sue', 'Rose'],
})
dl.write_deltalake(table_uri, df)
for person in [{'id': 3, 'name': 'Jake', }, {'id': 4, 'name': 'Sally'}, ]:
    df = pd.DataFrame([person])
    dl.write_deltalake(table_uri, df, mode='append')

# Create a Filter
filters = (pc.field("id") > pc.scalar(3))
dataset = deltaray.read_delta(table_uri, filters=filters, columns=['name'])
```

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

```shell
python setup.py bdist_wheel sdist
```

Installing Wheel:

```shell
pip install /path/to/wheel/..
```
