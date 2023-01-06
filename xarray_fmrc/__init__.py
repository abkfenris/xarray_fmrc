"""A lightweight way to manage forecast datasets using datatrees"""

from .accessor import FmrcAccessor
from .build_datatree import from_model_runs

__all__ = ["from_model_runs", "FmrcAccessor"]


try:
    from ._version import __version__
except ImportError:
    __version__ = "unknown"
