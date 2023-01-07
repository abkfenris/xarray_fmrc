"""
Handle forecast reference times
"""
import pandas as pd
import xarray as xr


def forecast_ref_time(ds: xr.Dataset) -> pd.Timestamp:
    """Get forecast reference time from coordinate or attribute"""
    try:
        return pd.to_datetime(ds["forecast_reference_time"].item())
    except KeyError:
        return pd.to_datetime(ds.attrs["forecast_reference_time"])
