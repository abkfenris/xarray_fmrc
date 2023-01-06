"""Build a forecast datatree from datasets"""
from typing import Set

from collections.abc import Iterable

import datatree
import pandas as pd
import xarray as xr


def from_model_runs(datasets: Iterable[xr.Dataset]) -> datatree.DataTree:
    """Build a datatree from a collection of Xarray Datasets

    Datasets are expected to have a single forecast_reference_time
    as a coordinate.
    """
    model_run_paths = []
    forecast_reference_times = []
    constant_forecast_times: Set[pd.Timestamp] = set()
    constant_offsets: Set[pd.Timedelta] = set()

    dt_dict = {}

    for ds in datasets:
        forecast_reference_time = pd.Timestamp(ds["forecast_reference_time"].item())
        path = f"model_run/{forecast_reference_time.isoformat()}"

        ds_times = ds["time"].to_numpy()

        constant_forecast_times = constant_forecast_times.union(set(ds_times))

        model_run_paths.append(path)
        forecast_reference_times.append(forecast_reference_time)

        td = ds["time"] - ds["forecast_reference_time"]
        td = pd.to_timedelta(td.to_series())

        constant_offsets = constant_offsets.union(set(td))

        dt_dict[path] = ds

    dt_dict["/"] = xr.Dataset(
        {
            "model_run_path": xr.DataArray(
                model_run_paths,
                dims=["forecast_reference_time"],
                coords={"forecast_reference_time": forecast_reference_times},
            ),
        },
        coords={
            "constant_forecast": pd.Series(list(constant_forecast_times)).sort_values(),
            "constant_offset": pd.Series(list(constant_offsets)).sort_values(),
        },
    )

    return datatree.DataTree.from_dict(dt_dict)