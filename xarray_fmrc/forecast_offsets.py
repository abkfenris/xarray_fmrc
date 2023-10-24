"""
Forecast offset handling
"""
import pandas as pd
import xarray as xr

from . import constants
from .forecast_reference_time import forecast_ref_time


def calc_offsets(
    ds: xr.Dataset,
    time_coord: str = constants.DEFAULT_TIME_COORD,
) -> pd.TimedeltaIndex:
    """Calculate forecast offsets in relation to reference time"""
    forecast_time = forecast_ref_time(ds)
    offsets = pd.to_datetime(ds[time_coord]) - forecast_time

    return offsets


def with_offsets(
    ds: xr.Dataset,
    time_coord: str = constants.DEFAULT_TIME_COORD,
) -> xr.Dataset:
    """Add forecast offset as a dimensionless coordinate"""
    offsets = calc_offsets(ds, time_coord=time_coord)

    ds = ds.assign_coords({"forecast_offset": (time_coord, offsets)})
    ds = ds.set_xindex("forecast_offset")
    return ds
