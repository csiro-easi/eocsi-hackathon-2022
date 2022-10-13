# Support functions for streamlit apps

import matplotlib.pyplot as plt
import xarray as xr
import io
from pathlib import Path
from functools import lru_cache

from datacube.drivers.netcdf import write_dataset_to_netcdf
from datacube.utils.cog import write_cog

# Caching is very helpful for streamlit apps, else xarray functions and figures will be re-run or recreated
# functools: cache and lru_cache
# - In-memory dict mapping arguments to variables. Arguments need to be dict-key hashable
# - cache = sensible defaults
# - lru_cache = set a maximum size (number of items)
# diskcache
# - On-disk sqlite DB. Pickles arguments and variables so more types are valid
# - Use fast (local) disk
#
# Can use both on-disk and in-memory caching, e.g.
# - local_cache = diskcache.Cache('/tmp/cache')
#
# @cache
# @local_cache.memoize()
# def myfunc(..):
try:
    from functools import cache  # Available from python 3.9
    import diskcache  # Available in EASI develop
except ImportError:
    pass


# A test file name for developers convenience
# /home/jovyan/landsat8_sr_ndvi.nc


def get_title() -> str:
    return '# :satellite: Satellite image viewer'

def get_logo() -> str:
    return '../resources/csiro_easi_logo.png'


@lru_cache(maxsize=128)  # Only hashable arg types
def read_user_xarray(filename: str) -> xr.Dataset:
    """Open the filename with xarray and return the xarray object, or an error string"""
    try:
        ds = xr.open_dataset(filename)
    except Exception as e:
        return str(e)
    return ds


# The following functions assume that filename is a valid xarray object

def xr_summary(filename: str) -> str:
    """Return a summary of the xarray object"""
    ds = read_user_xarray(filename)
    if isinstance(ds, str):
        return ds
    buffer = io.StringIO()
    ds.info(buffer)
    return buffer.getvalue()

def xr_times(filename: str) -> list:
    """Return a list of formatted datetime lables for the xarray object"""
    ds = read_user_xarray(filename)
    return ds.time.dt.strftime('%Y-%m-%dT%H:%M:%S').data.tolist()

def xr_bands(filename: str) -> list:
    """Return a list of variable or band lables for the xarray object"""
    ds = read_user_xarray(filename)
    return sorted(list(ds.keys()))


@lru_cache(maxsize=128)  # Only hashable arg types
def get_plot_for_timeslice(
    filename: str,
    band: str,
    index: str,
    vrng: tuple
) -> plt.Figure:
    """Create a matplotlib figure for the band and time index of the xarray object"""
    fig, axes = plt.subplots(figsize=(8, 6))
    ds = read_user_xarray(filename)
    timeslice = ds[band].isel(time=index)
    timeslice.plot(vmin=vrng[0], vmax=vrng[1], ax=axes)
    return fig


def write_file(
    filename: str,
    band: str,
    selected: list,
    write_file: str,
    overwrite: bool
) -> tuple:
    """Write the selected band and time indices to netCDF or COG files.
    Returns (success, message) tuple"""
    write_file = Path(write_file)
    if write_file.suffix not in ('.tif', '.nc'):
        return False, f'Choose a target file name ending with ".tif" or ".nc": {write_file.suffix}'
    ds = read_user_xarray(filename)
    try:
        if write_file.suffix == '.nc':
            if write_file.exists() and not overwrite:
                return False, 'File exists'
            ds_slice = ds[[band]].isel(time=selected)
            write_dataset_to_netcdf(ds_slice, write_file)
            msg = str(write_file)
        else: # COGs
            msg = []
            timestr = str(ds.time[1].dt.strftime('%Y%m%dT%H%M%S').data)
            for i in selected:
                singletimestamp_da = ds.isel(time=i).to_array()
                target = write_file.stem + f'-{timestr}.tif'
                msg.append(target)
                write_cog(
                    geo_im = singletimestamp_da,
                    fname = target,
                    overwrite = overwrite
                )
        return True, msg
    except Exception as e:
        return False, e
    
