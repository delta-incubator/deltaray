"""
Reading Delta Tables with Ray
"""
# Standard Libraries
from typing import Optional, List, Dict, Any, Tuple

# External Libraries
from deltalake import DeltaTable

from ray.data import read_parquet
from ray.data.dataset import Dataset
from ray.data.datasource import DefaultParquetMetadataProvider
from ray.data._internal.arrow_block import ArrowRow

import numpy as np


def read_delta(
    table_uri: str,
    *,
    version: Optional[str] = None,
    storage_options: Optional[Dict[str, str]] = None,
    without_files: bool = False,
    filesystem: Optional["pyarrow.fs.FileSystem"] = None,
    columns: Optional[List[str]] = None,
    parallelism: int = -1,
    ray_remote_args: Dict[str, Any] = None,
    tensor_column_schema: Optional[Dict[str, Tuple[np.dtype, Tuple[int, ...]]]] = None,
    meta_provider=DefaultParquetMetadataProvider(),
    **arrow_parquet_args,
) -> Dataset[ArrowRow]:
    """Create an Arrow dataset from a Delta Table using Ray

    Args:
        table_uri:
        version:
        storage_options:
        without_files:
        filesystem:
        columns:
        parallelism:
        ray_remote_args:
        tensor_column_schema:
        meta_provider:
        arrow_parquet_args:

    Returns:

    """
    dt = DeltaTable(table_uri, version, storage_options, without_files)
    return read_parquet(
        paths=dt.file_paths(),
        filesystem=filesystem,
        columns=columns,
        parallelism=parallelism,
        ray_remote_args=ray_remote_args,
        tensor_column_schema=tensor_column_schema,
        meta_provider=meta_provider,
        **arrow_parquet_args,
    )
