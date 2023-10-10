"""Build a forecast datatree from datasets"""
from typing import TYPE_CHECKING, Any, Dict, List, Optional

import datatree
import pandas as pd
import xarray as xr

if TYPE_CHECKING:
    from pandas.core.tools.datetimes import DatetimeScalar

from . import constants


def model_run_path(
    from_dt: "DatetimeScalar",
    group_prefix: str = constants.DEFAULT_GROUP_PREFIX,
    time_format: str = constants.DEFAULT_TIME_FORMAT,
) -> str:
    """Return the model run path given a datetime-like input of forecast_reference_time"""
    dt = pd.to_datetime(from_dt)

    return f"{group_prefix}{dt.strftime(time_format)}"


def forecast_reference_time_from_path(
    path: str,
    group_prefix: str = constants.DEFAULT_GROUP_PREFIX,
    time_format: str = constants.DEFAULT_TIME_FORMAT,
) -> pd.Timestamp:
    """Return the datasets forecast reference time based on it's path"""
    dt_str = path.removeprefix(f"/{group_prefix}")
    return pd.to_datetime(dt_str, format=time_format)


def from_dict(
    datasets: Dict["DatetimeScalar", xr.Dataset],
    group_prefix: str = constants.DEFAULT_GROUP_PREFIX,
    time_format: str = constants.DEFAULT_TIME_FORMAT,
    time_coord: Optional[str] = None,
    forecast_coords: Optional[List[str]] = None,
    tree_attrs: Optional[dict[str, Any]] = None,
) -> datatree.DataTree:
    """Build a datatree from a dictionary of forecast reference times to datasets"""
    path_dict = {}
    for dt, ds in datasets.items():
        path = model_run_path(dt, group_prefix, time_format)
        path_dict[path] = ds

    tree = datatree.DataTree.from_dict(path_dict)

    if tree_attrs is None:
        tree_attrs = {}

    tree_attrs[constants.DT_ATTR_GROUP_PREFIX] = group_prefix
    tree_attrs[constants.DT_ATTR_TIME_FORMAT] = time_format

    if time_coord:
        tree_attrs[constants.DT_ATTR_TIME_COORD] = time_coord

    if forecast_coords:
        tree_attrs[constants.DT_ATTR_FORECAST_COORDS] = forecast_coords

    tree.attrs = tree_attrs

    return tree
