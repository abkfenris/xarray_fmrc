# xarray-fmrc

<div align="center">

[![Tests](https://github.com/abkfenris/xarray_fmrc/actions/workflows/build.yml/badge.svg)](https://github.com/abkfenris/xarray_fmrc/actions/workflows/build.yml)
[![Python Version](https://img.shields.io/pypi/pyversions/xarray_fmrc.svg)](https://pypi.org/project/xarray-fmrc/)
[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/abkfenris/xarray-fmrc/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/abkfenris/xarray-fmrc/blob/master/.pre-commit-config.yaml)
[![Semantic Versions](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--versions-e10079.svg)](https://github.com/abkfenris/xarray-fmrc/releases)
[![License](https://img.shields.io/github/license/abkfenris/xarray_fmrc)](https://github.com/abkfenris/xarray_fmrc/blob/master/LICENSE)

Xarray-FMCR uses Xarray datatrees to provide a standard in-memory and storage representation of [Forecast Model Run Collections](http://www.unidata.ucar.edu/staff/caron/presentations/FmrcPoster.pdf) that can then be access via the various forecast views (best estimate/constant offset/constant time/model run).

</div>

```ipython
In [1]: import xarray as xr

In [2]: import xarray_fmrc

In [3]: ds0 = xr.open_dataset("fvcom_gom3_met_2022120118.nc")

In [4]: ds1 = xr.open_dataset("fvcom_gom3_met_2022121218.nc")

In [5]: dt = xarray_fmrc.from_model_runs([ds0, ds1])

In [6]: dt
Out[6]:
DataTree('None', parent=None)
│   Dimensions:                  (forecast_reference_time: 2,
│                                 constant_forecast: 242, constant_offset: 121)
│   Coordinates:
│     * forecast_reference_time  (forecast_reference_time) datetime64[ns] 2022-12...
│     * constant_forecast        (constant_forecast) datetime64[ns] 2022-12-02 .....
│     * constant_offset          (constant_offset) timedelta64[ns] 06:00:00 ... 5...
│   Data variables:
│       model_run_path           (forecast_reference_time) <U29 'model_run/2022-1...
└── DataTree('model_run')
    ├── DataTree('2022-12-01T18:00:00')
    │       Dimensions:                  (forecast_reference_time: 1, time: 121,
    │                                     latitude: 220, longitude: 215)
    │       Coordinates:
    │         * longitude                (longitude) float64 -79.95 -79.86 ... -60.13 -60.04
    │         * latitude                 (latitude) float64 27.03 27.12 ... 47.32 47.41
    │         * time                     (time) datetime64[ns] 2022-12-02 ... 2022-12-07
    │         * forecast_reference_time  (forecast_reference_time) datetime64[ns] 2022-12...
    │           forecast_offset          (time) timedelta64[ns] 06:00:00 ... 5 days 06:00:00
    │       Data variables:
    │           wind_speed               (forecast_reference_time, time, latitude, longitude) float32 ...
    │           wind_from_direction      (forecast_reference_time, time, latitude, longitude) float32 ...
    │       Attributes: (12/178)
    │           ...
    └── DataTree('2022-12-12T18:00:00')
            Dimensions:                  (forecast_reference_time: 1, time: 121,
                                          latitude: 220, longitude: 215)
            Coordinates:
              * longitude                (longitude) float64 -79.95 -79.86 ... -60.13 -60.04
              * latitude                 (latitude) float64 27.03 27.12 ... 47.32 47.41
              * time                     (time) datetime64[ns] 2022-12-13 ... 2022-12-18
              * forecast_reference_time  (forecast_reference_time) datetime64[ns] 2022-12...
                forecast_offset          (time) timedelta64[ns] 06:00:00 ... 5 days 06:00:00
            Data variables:
                wind_speed               (forecast_reference_time, time, latitude, longitude) float32 ...
                wind_from_direction      (forecast_reference_time, time, latitude, longitude) float32 ...
            Attributes: (12/178)
                ...

In [7]: dt.fmrc.constant_offset("12h")
Out[7]:
<xarray.Dataset>
Dimensions:                  (longitude: 215, latitude: 220,
                              forecast_reference_time: 2, time: 2)
Coordinates:
  * longitude                (longitude) float64 -79.95 -79.86 ... -60.13 -60.04
  * latitude                 (latitude) float64 27.03 27.12 ... 47.32 47.41
  * forecast_reference_time  (forecast_reference_time) datetime64[ns] 2022-12...
  * time                     (time) datetime64[ns] 2022-12-02T06:00:00 2022-1...
    forecast_offset          (time) timedelta64[ns] 12:00:00 12:00:00
Data variables:
    wind_speed               (forecast_reference_time, time, latitude, longitude) float32 ...
    wind_from_direction      (forecast_reference_time, time, latitude, longitude) float32 ...
Attributes: (12/178)
    ...
```

## Forecast views

![Forecast Model Run Collections](https://docs.unidata.ucar.edu/netcdf-java/current/userguide/images/netcdf-java/tutorial/feature_types/fmrc.png)

The various views are explained in more detail below, but each has a method on the `.fmrc` accessor that returns a dataset.

- `dt.fmrc.model_run(dt: str | datetime.datetime | pd.Timestamp) -> xr.Dataset`
- `dt.fmrc.constant_offset(offset: str | datetime.timedelta | pd.TimeOffset?) -> xr.Dataset`
- `dt.fmrc.constant_forecast(dt: str | datetime.datetime | pd.Timestamp) -> xr.Dataset`

_everything below are just ideas or placeholders at this point_

- `dt.fmrc.best() -> xr.Dataset`

## Kerchunk

Kerchunk has the ability to break down [chunks into smaller chunks](https://fsspec.github.io/kerchunk/reference.html#kerchunk.utils.subchunk). Xarray-FMRC could provide utilities to take a collection of kerchunk files, break them apart, and rebuild them in the various FMRC views.

## Xpublish-FMRC

Xpublish-FMRC provides new endpoints for xpublish servers to serve forecast model run collections.

This uses the plugin interface to create a new top level path, and then other dataset plugins to serve various forecast views. For each dataset plugin registered below it, it overrides the `get_dataset` function.

- `forecasts/gfs/best/edr/position`
- `forecasts/gfs/model_run/20230101/edr/position`
- `forecasts/gfs/constant_forecast/20230101/edr/position`
- `forecasts/gfs/constant_offset/6h/edr/position`


## FMRC Dataset View definitions

_There may be a better name for these, but my brain is currently comparing them to database views._

_Definitions pulled from http://www.unidata.ucar.edu/staff/caron/presentations/FmrcPoster.pdf_

### Model Run Datasets

The RUC model is run hourly, and 12 runs are show
in this collection; note that different runs contain
forecast hours. The complete results for a single ru
model run dataset.
The selected example here is the run made on
2006-12-11 06:00 Z, having forecasts at
0,1,2,3,4,5,6,7,8,9 and 12 hours.

### Constant forecast/valid time dataset

A __constant forecast__ dataset is created from all data that have the same forecast/valid time. Using the 0 hour analysis as the best state estimate, one can use this dataset to evaluate how accurate forecasts are.

The selected example here is for the forecast time 2006-12-11 12:00 Z, using forecasts from the runs made at 0, 3, 6, 9, 10, 11, and 12 Z. There are a total of 24 such datasets in this collection.

### Constant forecast offset datasets

A __constant offset__ dataset is created from all the data that have the same offset time. This collection has 11 such datasets: the 0, 1, 2, 3, 4, 5, 5, 6, 8, 9, and 12 hour offsets.

The selected example here is for the 6 hour offset using forecast from the runs made at 0, 3, 6, 9, and 12 Z.

### Best estimate dataset

For each forecast time in the collection, the best estimate for that hour is used to create the __best estimate__ dataset, which covers the entire time range of the collection.

For this example, the best estimate is the 0 hour analysis from each run, plus all the forecasts from the latest run.
