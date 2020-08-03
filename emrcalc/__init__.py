"""
Initialize class emrcalc
"""

try:
    __version__ = get_distribution('emrcalc').version
except DistributionNotFound:
    __version__ = '*NOT INSTALLED*'

from . import *

