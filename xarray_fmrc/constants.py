"""
Constant and default values for attributes and other configuration of
xarray_fmrc.
"""

DEFAULT_GROUP_PREFIX = "forecast_reference_time/"
DEFAULT_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S"
DEFAULT_TIME_COORD = "time"
DEFAULT_FORECAST_COORDS = ["forecast_reference_time", "forecast_offset"]

DT_ATTR_GROUP_PREFIX = "xarray_fmrc_group_prefix"
DT_ATTR_TIME_FORMAT = "xarray_fmrc_time_format"
DT_ATTR_TIME_COORD = "xarray_fmrc_time_coord"
DT_ATTR_FORECAST_COORDS = "xarray_fmrc_forecast_coords"


DT_ATTRS = {
    "group_prefix": DT_ATTR_GROUP_PREFIX,
    "time_format": DT_ATTR_TIME_FORMAT,
    "time_coord": DT_ATTR_TIME_COORD,
    "forecast_coords": DT_ATTR_FORECAST_COORDS,
}
