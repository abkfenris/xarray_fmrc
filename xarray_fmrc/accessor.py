"""
xarray-datatree accessor to provide access to
forecast model run collections
"""
from typing import TYPE_CHECKING, Union

from datetime import timedelta

import datatree
import pandas as pd
import xarray as xr

from . import constants
from .build_datatree import forecast_reference_time_from_path, model_run_path
from .forecast_offsets import with_offsets

if TYPE_CHECKING:
    from pandas.core.tools.datetimes import DatetimeScalar


@datatree.register_datatree_accessor("fmrc")
class FmrcAccessor:
    """
    xarray-datatree accessor to provide access to
    forecast model run collections
    """

    time_coord = constants.DEFAULT_TIME_COORD
    group_prefix = constants.DEFAULT_GROUP_PREFIX
    time_format = constants.DEFAULT_TIME_FORMAT
    forecast_coords = constants.DEFAULT_FORECAST_COORDS

    def __init__(self, datatree_obj: datatree.DataTree):
        """Set the internal datatree object, and if any of the top level attrs are set,
        override the defaults"""
        self._datatree_obj = datatree_obj

        for key, value in constants.DT_ATTRS.items():
            if value in datatree_obj.attrs:
                setattr(self, key, datatree_obj.attrs[value])

    def model_run_path(self, from_dt: "DatetimeScalar") -> str:
        """Return the model run path given a datetime-like input"""
        return model_run_path(from_dt, self.group_prefix, self.time_format)

    def model_run(self, dt: "DatetimeScalar") -> xr.Dataset:
        """Get the dataset for a single model run

        Accepts valid to `pd.to_datetime()`
        https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.to_datetime.html
        """
        path = self.model_run_path(dt)

        return self._datatree_obj[path].ds

    def forecast_reference_time_from_path(self, path: str) -> pd.Timestamp:
        """Return the forecast reference time for a given path"""
        return forecast_reference_time_from_path(
            path,
            self.group_prefix,
            self.time_format,
        )

    def forecast_reference_times(self):
        """Get the forecast reference times based on the pattern in the path"""
        times = {}

        for group in self._datatree_obj.groups:
            try:
                times[group] = self.forecast_reference_time_from_path(group)
            except ValueError:
                pass

        return times

    def constant_forecast(self, dt: "DatetimeScalar") -> xr.Dataset:
        """
        Returns a dataset for a single time, from all forecast model runs.

        Accepts valid to `pd.to_datetime()`
        https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.to_datetime.html
        """
        datetime = pd.to_datetime(dt)
        filtered_ds = []

        for t in sorted(self.forecast_reference_times().values()):
            ds = self.model_run(t)

            try:
                ds = ds.sel({self.time_coord: datetime})
                ds = (
                    ds.drop_indexes(self.forecast_coords)
                    .reset_coords(self.forecast_coords)
                    .squeeze()
                )
                ds["forecast_reference_time"] = t
                filtered_ds.append(ds)
            except KeyError:
                pass

        combined = xr.concat(filtered_ds, "forecast_reference_time")
        combined = combined.sortby("forecast_reference_time")
        return combined

    def constant_offset(self, offset: Union[str, int, float, timedelta]) -> xr.Dataset:
        """
        Returns a dataset with the same offset from the forecasted time.

        Accepts inputs to `pd.to_timedelta()`
        https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.to_timedelta.html
        """
        timedelta = pd.to_timedelta(offset)

        filtered_ds = []

        for t in sorted(self.forecast_reference_times().values()):
            ds = self.model_run(t)
            ds = (
                ds.drop_indexes(self.forecast_coords)
                .reset_coords(self.forecast_coords)
                .squeeze()
            )
            ds["forecast_reference_time"] = t
            ds = with_offsets(ds, self.time_coord)

            try:
                ds = ds.sel(forecast_offset=timedelta)

                filtered_ds.append(ds)
            except KeyError:
                pass

        combined = xr.concat(filtered_ds, self.time_coord)
        combined = combined.sortby(self.time_coord)
        return combined

    def best(self) -> xr.Dataset:
        """
        Returns a dataset with the best possible forecast data.
        """
        forecast_times = sorted(self.forecast_reference_times().values(), reverse=True)

        dataset: xr.Dataset = None

        for t in forecast_times:
            ds = self.model_run(t)
            ds = (
                ds.drop_indexes(self.forecast_coords)
                .reset_coords(self.forecast_coords)
                .squeeze()
            )
            ds["forecast_reference_time"] = t

            if dataset is None:
                dataset = ds
            else:
                existing_times = set(dataset[self.time_coord].to_numpy())
                new_times = set(ds[self.time_coord].to_numpy())
                unique_times = new_times.difference(existing_times)

                ds = ds.sel({self.time_coord: sorted(unique_times)})

                dataset = xr.concat([dataset, ds], self.time_coord)

        dataset = dataset.sortby(self.time_coord)
        return dataset
