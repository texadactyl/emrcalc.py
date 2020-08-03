"""
Initialize class emrcalc
"""

from pkg_resources import get_distribution, DistributionNotFound

try:
    __version__ = get_distribution('emrcalc').version
except DistributionNotFound:
    __version__ = '*NOT INSTALLED*'

from . import *

