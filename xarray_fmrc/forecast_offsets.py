"""
Forecast offset handling
"""
import pandas as pd
import xarray as xr

from .forecast_reference_time import forecast_ref_time


def calc_offsets(ds: xr.Dataset) -> pd.TimedeltaIndex:
    """Calculate forecast offsets in relation to reference time"""
    forecast_time = forecast_ref_time(ds)
    offsets = pd.to_datetime(ds["time"]) - forecast_time

    return offsets


def with_offsets(ds: xr.Dataset) -> xr.Dataset:
    """Add forecast offset as a dimensionless coordinate"""
    offsets = calc_offsets(ds)

    return ds.assign_coords({"forecast_offset": ("time", offsets)})
