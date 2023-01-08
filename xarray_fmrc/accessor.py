"""
xarray-datatree accessor to provide access to
forecast model run collections
"""
from typing import TYPE_CHECKING, Union

from datetime import timedelta

import datatree
import pandas as pd
import xarray as xr

from .build_datatree import model_run_path
from .forecast_reference_time import forecast_ref_time

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
        datetime = pd.to_datetime(dt)
        filtered_ds = []

        for child in self.datatree_obj["model_run"].children.values():
            try:
                selected = child.ds.sel(time=datetime)
                filtered_ds.append(selected)
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

        for child in self.datatree_obj["model_run"].children.values():
            try:
                selected = child.ds.sel(forecast_offset=timedelta)
                filtered_ds.append(selected)
            except KeyError:
                pass

        combined = xr.concat(filtered_ds, "time")
        combined = combined.sortby("time")
        return combined

    def best(self) -> xr.Dataset:
        """
        Returns a dataset with the best possible forecast data.
        """
        forecast_coords = ["forecast_reference_time", "forecast_offset"]

        forecast_times = self.datatree_obj["forecast_reference_time"].sortby(
            "forecast_reference_time",
            ascending=False,
        )

        dataset: xr.Dataset = None

        for t in forecast_times:
            ft = forecast_ref_time(t)

            ds = self.datatree_obj[f"model_run/{ft.isoformat()}"].ds
            ds = (
                ds.drop_indexes(forecast_coords).reset_coords(forecast_coords).squeeze()
            )

            if dataset is None:
                dataset = ds
            else:
                existing_times = set(dataset["time"].to_numpy())
                new_times = set(ds["time"].to_numpy())
                unique_times = new_times.difference(existing_times)

                ds = ds.where(ds["time"].isin(list(unique_times)))

                dataset = xr.concat([dataset, ds], "time")

        dataset = dataset.sortby("time")
        return dataset
