"""A lightweight way to manage forecast datasets using datatrees"""

from .accessor import FmrcAccessor
from .build_datatree import from_dict

__all__ = ["from_dict", "FmrcAccessor"]


try:
    from ._version import __version__
except ImportError:
    __version__ = "unknown"
