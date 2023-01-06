"""
xarray-datatree accessor to provide access to
forecast model run collections
"""
from typing import TYPE_CHECKING, Union

from datetime import timedelta

import datatree
import xarray as xr

from .build_datatree import model_run_path

if TYPE_CHECKING:
    from pandas.core.tools.datetimes import DatetimeScalar


@datatree.register_datatree_accessor("fmrc")
class FmrcAccessor:
    """
    xarray-datatree accessor to provide access to
    forecast model run collections
    """

    def __init__(self, datatree_obj: datatree.DataTree):
        self.datatree_obj = datatree_obj

    def model_run(self, dt: "DatetimeScalar") -> xr.Dataset:
        """Get the dataset for a single model run

        Accepts valid to `pd.to_datetime()`
        https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.to_datetime.html
        """
        path = model_run_path(dt)

        return self.datatree_obj[path].ds

    def constant_forecast(self, dt: "DatetimeScalar") -> xr.Dataset:
        """
        Returns a dataset for a single time, from all forecast model runs.

        Accepts valid to `pd.to_datetime()`
        https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.to_datetime.html
        """
        raise NotImplementedError

    def constant_offset(self, offset: Union[str, int, float, timedelta]) -> xr.Dataset:
        """
        Returns a dataset with the same offset from the forecasted time.

        Accepts inputs to `pd.to_timedelta()`
        https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.to_timedelta.html
        """
        raise NotImplementedError

    def best(self) -> xr.Dataset:
        """
        Returns a dataset with the best possible forecast data.
        """
        raise NotImplementedError
