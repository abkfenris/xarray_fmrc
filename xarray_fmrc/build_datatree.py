"""Build a forecast datatree from datasets"""
from typing import TYPE_CHECKING, Set

from collections.abc import Iterable

import datatree
import pandas as pd
import xarray as xr

if TYPE_CHECKING:
    from pandas.core.tools.datetimes import DatetimeScalar


def model_run_path(from_dt: DatetimeScalar) -> str:
    """Return the model run path given a datetime-like input"""
    dt = pd.to_datetime(from_dt)

    return f"model_run/{dt.isoformat()}"


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
        path = model_run_path(forecast_reference_time)

        ds_times = ds["time"].to_numpy()

        constant_forecast_times = constant_forecast_times.union(set(ds_times))

        model_run_paths.append(path)
        forecast_reference_times.append(forecast_reference_time)

        td = ds["time"] - ds["forecast_reference_time"]
        td = pd.to_timedelta(td.to_series())

        constant_offsets = constant_offsets.union(set(td))

        dt_dict[path] = ds

    root_ds = xr.Dataset(
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
    root_ds = root_ds.sortby("forecast_reference_time")

    dt_dict["/"] = root_ds

    return datatree.DataTree.from_dict(dt_dict)
