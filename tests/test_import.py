"""
Note: `deltaray` does not currently use all DAT tests available

    `deltaray` only uses the following:
    - all_primitive_types

    `deltaray` needs to test these additional DAT tables:
    - basic_append
    - basic_partitioned
    - multi_partitioned
    - multi_partitioned_2
    - nested_types
    - no_replay
    - no_stats
    - stats_as_struct
    - with_checkpoint
    - with_schema_change

Tables that aren't currently being tested cover a capability currently lacking in `deltaray`
"""
# Standard Libraries
import tempfile

# External Libraries
import ray
import pytest
import pandas as pd
import deltalake as dl

# Internal Libraries
import deltaray


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


def test_reader_all_primitive_types(ray_cluster):
    table_uri = './tests/reader_tests/generated/all_primitive_types/delta'
    parquet_uri = './tests/reader_tests/generated/all_primitive_types/expected/latest/table_content/part-00000-2acd2058-e58d-4535-bb8b-6ed3bb27a955-c000.snappy.parquet'

    actual_df = deltaray.read_delta(table_uri).to_pandas()
    expected_df = ray.data.read_parquet(parquet_uri).to_pandas()
    assert actual_df.compare(expected_df).empty
