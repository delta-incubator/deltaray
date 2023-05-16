"""
Note: `deltaray` does not currently use all DAT tests available

`deltaray` uses the following DAT tables:
- all_primitive_types
- basic_append
- basic_partitioned
- no_replay
- stats_as_struct
- with_checkpoint
- with_schema_change

`deltaray` needs to test these additional DAT tables:
- multi_partitioned: Escaped characters in data file paths aren't yet handled (#1079)
- multi_partitioned_2: waiting for PyArrow 11.0.0 for decimal cast support (#1078)
- nested_types: waiting for PyArrow 11.0.0 so we can ignore internal field names in equality
- no_stats: we don't yet support files without stats (#582)
"""
# Standard Libraries
import tempfile
import json
from pathlib import Path
from typing import Any, Dict, NamedTuple, Optional

# External Libraries
import ray
import pyarrow.parquet as pq
import pytest
import pandas as pd
import deltalake as dl

# Internal Libraries
import deltaray


class ReadCase(NamedTuple):
    root: Path
    version: Optional[int]
    case_info: Dict[str, Any]
    version_metadata: Dict[str, Any]


cases = []
failing_cases = {
    "multi_partitioned_2": "Waiting for PyArrow 11.0.0 for decimal cast support (#1078)",
    "nested_types": "Waiting for PyArrow 11.0.0 so we can ignore internal field names in equality",
    "multi_partitioned": "Escaped characters in data file paths aren't yet handled (#1079)",
    "no_stats": "We don't yet support files without stats (#582)",
}
dat_version = "0.0.2"
reader_case_path = Path("tests/reader_tests/generated")
for path in reader_case_path.iterdir():
    if path.is_dir():
        with open(path / "test_case_info.json") as f:
            metadata = json.load(f)
        for version_path in (path / "expected").iterdir():
            if path.name.startswith("v"):
                version = int(path.name[1:])
            else:
                version = None
            with open(version_path / "table_version_metadata.json") as f:
                version_metadata = json.load(f)
        cases.append(ReadCase(path, version, metadata, version_metadata))


@pytest.fixture(scope='session')
def ray_cluster():
    # Start the Ray Cluster
    ray.init(num_cpus=1)

    # Yield control back to test
    yield

    # Stop Ray cluster
    ray.shutdown()


def test_import():
    from deltaray import read_delta


def test_ray_cluster(ray_cluster):
    @ray.remote
    def identity(x):
        return x

    result = ray.get(identity.remote(42))
    assert result == 42


def test_read_deltatable(ray_cluster):
    with tempfile.TemporaryDirectory() as tmp:
        table_uri = f'{tmp}/delta-table'
        df = pd.DataFrame({'id': [0, 1, 2, ], })
        dl.write_deltalake(table_uri, df)

        ds = deltaray.read_delta(table_uri)
        df_read = ds.to_pandas()

    assert df.equals(df_read)


@pytest.mark.parametrize(
    "case", cases, ids=lambda case: f"{case.case_info['name']} (version={case.version})"
)
def test_dat(case: ReadCase, ray_cluster):
    root, version, case_info, version_metadata = case

    if case_info['name'] in failing_cases:
        msg = failing_cases[case_info['name']]
        pytest.skip(msg)

    # Get paths to Delta and Parquet Tables
    delta_root = root / "delta"
    version_path = 'latest' if version is None else f'v{version}'
    parquet_root = root / 'expected' / version_path / 'table_content'

    # Read and compare Delta and Parquet Tables
    actual = deltaray.read_delta(str(delta_root), version=version).to_pandas()
    expected = pq.read_table(parquet_root).to_pandas()
    assert_tables_equal(expected, actual)


def assert_tables_equal(first: pd.DataFrame, second: pd.DataFrame) -> None:
    first.sort_index(axis=1, inplace=True)
    first_sorted = first.sort_values(by=first.columns[0]).reset_index(drop=True)
    second.sort_index(axis=1, inplace=True)
    second_sorted = second.sort_values(by=second.columns[0]).reset_index(drop=True)
    assert first_sorted.compare(second_sorted).empty
