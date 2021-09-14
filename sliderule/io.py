# Copyright (c) 2021, University of Washington
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the University of Washington nor the names of its
#    contributors may be used to endorse or promote products derived from this
#    software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE UNIVERSITY OF WASHINGTON AND CONTRIBUTORS
# “AS IS” AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
# TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE UNIVERSITY OF WASHINGTON OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import warnings
import datetime
import scipy.io
import geopandas
import h5py
import numpy as np

# attributes for ATL06-SR variables
def get_attributes():
    attrs = {}
    # file level attributes
    attrs['featureType'] = 'trajectory'
    attrs['title'] = "ATLAS/ICESat-2 SlideRule Height"
    attrs['reference'] = 'https://doi.org/10.5281/zenodo.5484048'
    attrs['date_created'] = datetime.datetime.now().isoformat()
    attrs['geospatial_lat_units'] = "degrees_north"
    attrs['geospatial_lon_units'] = "degrees_east"
    attrs['geospatial_ellipsoid'] = "WGS84"
    attrs['date_type'] = "UTC"
    attrs['time_type'] = "CCSDS UTC-A"
    # segment ID
    attrs['segment_id'] = {}
    attrs['segment_id']['long_name'] = "Along-track segment ID number"
    attrs['segment_id']['coordinates'] = "latitude longitude"
    # delta time
    attrs['delta_time'] = {}
    attrs['delta_time']['units'] = "seconds since 2018-01-01"
    attrs['delta_time']['long_name'] = "Elapsed GPS seconds"
    attrs['delta_time']['standard_name'] = "time"
    attrs['delta_time']['calendar'] = "standard"
    attrs['delta_time']['coordinates'] = "latitude longitude"
    # latitude
    attrs['latitude'] = {}
    attrs['latitude']['units'] = "degrees_north"
    attrs['latitude']['long_name'] = "Latitude"
    attrs['latitude']['standard_name'] = "latitude"
    attrs['latitude']['valid_min'] = -90.0
    attrs['latitude']['valid_max'] = 90.0
    # longitude
    attrs['longitude'] = {}
    attrs['longitude']['units'] = "degrees_east"
    attrs['longitude']['long_name'] = "Longitude"
    attrs['longitude']['standard_name'] = "longitude"
    attrs['longitude']['valid_min'] = -180.0
    attrs['longitude']['valid_max'] = 180.0
    # mean height from fit
    attrs['h_mean'] = {}
    attrs['h_mean']['units'] = "meters"
    attrs['h_mean']['long_name'] = "Height Mean"
    attrs['h_mean']['coordinates'] = "latitude longitude"
    # uncertainty in mean height
    attrs['h_sigma'] = {}
    attrs['h_sigma']['units'] = "meters"
    attrs['h_sigma']['long_name'] = "Height Error"
    attrs['h_sigma']['coordinates'] = "latitude longitude"
    # RMS of fit
    attrs['rms_misfit'] = {}
    attrs['rms_misfit']['units'] = "meters"
    attrs['rms_misfit']['long_name'] = "RMS of fit"
    attrs['rms_misfit']['coordinates'] = "latitude longitude"
    # along track slope
    attrs['dh_fit_dx'] = {}
    attrs['dh_fit_dx']['units'] = "meters/meters"
    attrs['dh_fit_dx']['contentType'] = "modelResult"
    attrs['dh_fit_dx']['long_name'] = "Along Track Slope"
    attrs['dh_fit_dx']['coordinates'] = "latitude longitude"
    # across track slope
    attrs['dh_fit_dy'] = {}
    attrs['dh_fit_dy']['units'] = "meters/meters"
    attrs['dh_fit_dy']['long_name'] = "Across Track Slope"
    attrs['dh_fit_dy']['coordinates'] = "latitude longitude"
    # number of photons in fit
    attrs['n_fit_photons'] = {}
    attrs['n_fit_photons']['units'] = "1"
    attrs['n_fit_photons']['long_name'] = "Number of Photons in Fit"
    attrs['n_fit_photons']['coordinates'] = "latitude longitude"
    # surface fit window
    attrs['w_surface_window_final'] = {}
    attrs['w_surface_window_final']['units'] = "meters"
    attrs['w_surface_window_final']['long_name'] = "Surface Window Width"
    attrs['w_surface_window_final']['coordinates'] = "latitude longitude"
    # robust dispersion estimate of fit
    attrs['h_robust_sprd'] = {}
    attrs['h_robust_sprd']['units'] = "meters"
    attrs['h_robust_sprd']['long_name'] = "Robust Spread"
    attrs['h_robust_sprd']['coordinates'] = "latitude longitude"
    # orbital cycle
    attrs['cycle'] = {}
    attrs['cycle']['long_name'] = "Orbital cycle"
    attrs['cycle']['coordinates'] = "latitude longitude"
    # RGT
    attrs['rgt'] = {}
    attrs['rgt']['long_name'] = "Reference Ground Track"
    attrs['rgt']['coordinates'] = "latitude longitude"
    # ground track
    attrs['gt'] = {}
    attrs['gt']['long_name'] = "Ground track identifier"
    attrs['gt']['flag_values'] = [10, 20, 30, 40, 50, 60]
    attrs['gt']['flag_meanings'] = "GT1L, GT1R, GT2L, GT2R, GT3L, GT3R"
    attrs['gt']['valid_min'] = 10
    attrs['gt']['valid_max'] = 60
    # spot
    attrs['spot'] = {}
    attrs['spot']['long_name'] = "ATLAS spot number"
    attrs['spot']['coordinates'] = "latitude longitude"
    attrs['spot']['valid_min'] = 1
    attrs['spot']['valid_max'] = 6
    # pflags
    attrs['pflags'] = {}
    attrs['pflags']['long_name'] = "Processing Flags"
    attrs['pflags']['coordinates'] = "latitude longitude"
    attrs['pflags']['flag_values'] = [0, 1, 2, 4]
    attrs['pflags']['flag_meanings'] = ("valid, spread too short, "
        "too few photons, max iterations reached")
    attrs['pflags']['valid_min'] = 0
    attrs['pflags']['valid_max'] = 4
    # return the attributes for the sliderule variables
    return attrs

# extract coordinates from a sliderule region
def coordinates(polygon):
    npts = len(polygon)
    x = np.zeros((npts))
    y = np.zeros((npts))
    for i,p in enumerate(polygon):
        x[i] = p['lon']
        y[i] = p['lat']
    return (x,y)

# output geodataframe to netCDF (version 3)
def to_nc(gdf, filename, **kwargs):
    # set default keyword arguments
    kwargs.setdefault('parameters',None)
    kwargs.setdefault('regions',[])
    kwargs.setdefault('verbose',False)
    # get output attributes
    attributes = get_attributes()
    # open netCDF3 file object (64-bit offset format)
    fileID = scipy.io.netcdf.netcdf_file(filename, 'w', version=2)
    # convert geodataframe to pandas dataframe
    df = geopandas.pd.DataFrame(gdf.drop(columns='geometry'))
    # append latitude and longitude as columns
    df['latitude'] = gdf['geometry'].values.y
    df['longitude'] = gdf['geometry'].values.x
    # create dimensions
    fileID.createDimension('delta_time', len(df['delta_time']))
    # for each variable in the dataframe
    for key,val in df.items():
        if np.issubdtype(val, np.unsignedinteger):
            nc = fileID.createVariable(key, 'i4', ('delta_time',))
            nc[:] = val.astype(np.int32)
        else:
            nc = fileID.createVariable(key, val.dtype, ('delta_time',))
            nc[:] = val.copy()
        # set attributes for variable
        for att_key,att_val in attributes[key].items():
            setattr(nc,att_key,att_val)
    # add file attributes
    fileID.featureType = attributes['featureType']
    fileID.title = attributes['title']
    fileID.reference = attributes['reference']
    fileID.date_created = attributes['date_created']
    fileID.geospatial_lat_units = attributes['geospatial_lat_units']
    fileID.geospatial_lon_units = attributes['geospatial_lon_units']
    fileID.geospatial_ellipsoid = attributes['geospatial_ellipsoid']
    fileID.date_type = attributes['date_type']
    fileID.time_type = attributes['time_type']
    # add each parameter as an attribute
    SRparams = ['H_min_win', 'atl08_class', 'ats', 'cnf', 'cnt', 'len',
        'maxi', 'res', 'sigma_r_max', 'srt']
    # for each adjustable sliderule parameter
    for p in SRparams:
        # try to get the parameter if available
        try:
            setattr(fileID, p, kwargs['parameters'][p])
        except:
            # if empty or unavailable
            pass
    # save each region as a list attribute
    for i,poly in enumerate(kwargs['regions']):
        lon,lat = coordinates(poly)
        setattr(fileID, 'poly{0:d}_x'.format(i), lon)
        setattr(fileID, 'poly{0:d}_y'.format(i), lat)
    # Output netCDF structure information
    if kwargs['verbose']:
        print(filename)
        print(list(fileID.variables.keys()))
    # Closing the netCDF file
    fileID.close()

# input geodataframe from netCDF (version 3)
def from_nc(filename, **kwargs):
    # open netCDF3 file object (64-bit offset format)
    fileID = scipy.io.netcdf.netcdf_file(filename, 'r', version=2)
    warnings.filterwarnings("ignore")
    # input dictionary for input variables
    nc = {}
    # get each variable from netCDF
    for key,val in fileID.variables.items():
        # swap byte order to little endian if big endian
        flattened = val[:].squeeze()
        if (flattened.dtype.byteorder == '>'):
            nc[key] = flattened.byteswap().newbyteorder()
        else:
            nc[key] = flattened.copy()
    # Closing the netCDF file
    fileID.close()
    warnings.filterwarnings("default")
    # Generate Time Column
    delta_time = (nc['delta_time']*1e9).astype('timedelta64[ns]')
    atlas_sdp_epoch = np.datetime64(datetime.datetime(2018, 1, 1))
    nc['time'] = geopandas.pd.to_datetime(atlas_sdp_epoch + delta_time)
    # generate geometry column
    geometry = geopandas.points_from_xy(nc['longitude'], nc['latitude'])
    del nc['longitude']
    del nc['latitude']
    # create Pandas DataFrame object
    df = geopandas.pd.DataFrame(nc)
    # build GeoDataFrame
    gdf = geopandas.GeoDataFrame(df, geometry=geometry)
    # set index
    gdf.set_index('time', inplace=True)
    gdf.sort_index(inplace=True)
    # return geodataframe
    return gdf

# output geodataframe to HDF5
def to_hdf(gdf, filename, **kwargs):
    # set default keyword arguments
    kwargs.setdefault('driver','pytables')
    kwargs.setdefault('parameters',None)
    kwargs.setdefault('regions',[])
    kwargs.setdefault('verbose',False)
    # get output attributes
    attributes = get_attributes()
    # convert geodataframe to pandas dataframe
    df = geopandas.pd.DataFrame(gdf.drop(columns='geometry'))
    # append latitude and longitude as columns
    df['latitude'] = gdf['geometry'].values.y
    df['longitude'] = gdf['geometry'].values.x
    # output to HDF5 format
    if (kwargs['driver'].lower() == 'pytables'):
        kwargs.pop('driver')
        # write dataframe to pytables HDF5
        write_pytables(df, filename, attributes, **kwargs)
    elif (kwargs['driver'].lower() == 'h5py'):
        kwargs.pop('driver')
        # write dataframe to HDF5
        write_h5py(df, filename, attributes, **kwargs)

# write pandas dataframe to pytables HDF5
def write_pytables(df, filename, attributes, **kwargs):
    # set default keyword arguments
    kwargs.setdefault('parameters',None)
    kwargs.setdefault('regions',[])
    kwargs.setdefault('verbose',False)
    # write data to a pytables HDF5 file
    df.to_hdf(filename, 'sliderule_segments', format="table", mode="w")
    # add file attributes
    fileID = geopandas.pd.HDFStore(filename, mode='a')
    fileID.root._v_attrs.TITLE = attributes['title']
    fileID.root._v_attrs.reference = attributes['reference']
    fileID.root._v_attrs.date_created = attributes['date_created']
    fileID.root._v_attrs.geospatial_lat_units = attributes['geospatial_lat_units']
    fileID.root._v_attrs.geospatial_lon_units = attributes['geospatial_lon_units']
    fileID.root._v_attrs.geospatial_ellipsoid = attributes['geospatial_ellipsoid']
    fileID.root._v_attrs.date_type = attributes['date_type']
    fileID.root._v_attrs.time_type = attributes['time_type']
    # add each parameter as an attribute
    SRparams = ['H_min_win', 'atl08_class', 'ats', 'cnf', 'cnt', 'len',
        'maxi', 'res', 'sigma_r_max', 'srt']
    # for each adjustable sliderule parameter
    for p in SRparams:
        # try to get the parameter if available
        try:
            setattr(fileID.root._v_attrs, p, kwargs['parameters'][p])
        except:
            # if empty or unavailable
            pass
    # save each region as a list attribute
    for i,poly in enumerate(kwargs['regions']):
        lon,lat = coordinates(poly)
        setattr(fileID.root._v_attrs, 'poly{0:d}_x'.format(i), lon)
        setattr(fileID.root._v_attrs, 'poly{0:d}_y'.format(i), lat)
    # Output HDF5 structure information
    if kwargs['verbose']:
        print(filename)
        print(fileID.get_storer('sliderule_segments').non_index_axes[0][1])
    # Closing the HDF5 file
    fileID.close()

# write pandas dataframe to h5py HDF5
def write_h5py(df, filename, attributes, **kwargs):
    # set default keyword arguments
    kwargs.setdefault('parameters',None)
    kwargs.setdefault('regions',[])
    kwargs.setdefault('verbose',False)
    # open HDF5 file object
    fileID = h5py.File(filename, mode='w')
    # create HDF5 records
    h5 = {}
    # create dataset for variable
    key = 'delta_time'
    h5[key] = fileID.create_dataset(key, df[key].shape, data=df[key],
        dtype=df[key].dtype, compression='gzip')
    # set attributes for variable
    for att_key,att_val in attributes[key].items():
        h5[key].attrs[att_key] = att_val
    # for each variable in the dataframe
    for key,val in df.items():
        # skip delta time variable
        if (key == 'delta_time'):
            continue
        # create dataset for variable
        h5[key] = fileID.create_dataset(key, val.shape, data=val,
            dtype=val.dtype, compression='gzip')
        h5[key].dims[0].attach_scale(h5['delta_time'])
        # set attributes for variable
        for att_key,att_val in attributes[key].items():
            h5[key].attrs[att_key] = att_val
    # add file attributes
    fileID.attrs['featureType'] = attributes['featureType']
    fileID.attrs['title'] = attributes['title']
    fileID.attrs['reference'] = attributes['reference']
    fileID.attrs['date_created'] = attributes['date_created']
    fileID.attrs['geospatial_lat_units'] = attributes['geospatial_lat_units']
    fileID.attrs['geospatial_lon_units'] = attributes['geospatial_lon_units']
    fileID.attrs['geospatial_ellipsoid'] = attributes['geospatial_ellipsoid']
    fileID.attrs['date_type'] = attributes['date_type']
    fileID.attrs['time_type'] = attributes['time_type']
    # add each parameter as an attribute
    SRparams = ['H_min_win', 'atl08_class', 'ats', 'cnf', 'cnt', 'len',
        'maxi', 'res', 'sigma_r_max', 'srt']
    # for each adjustable sliderule parameter
    for p in SRparams:
        # try to get the parameter if available
        try:
            fileID.attrs[p] = kwargs['parameters'][p]
        except:
            # if empty or unavailable
            pass
    # save each region as a list attribute
    for i,poly in enumerate(kwargs['regions']):
        lon,lat = coordinates(poly)
        fileID.attrs['poly{0:d}_x'.format(i)] = lon.copy()
        fileID.attrs['poly{0:d}_y'.format(i)] = lat.copy()
    # Output HDF5 structure information
    if kwargs['verbose']:
        print(filename)
        print(list(fileID.keys()))
    # Closing the HDF5 file
    fileID.close()

# input geodataframe from HDF5
def from_hdf(filename, **kwargs):
    # set default keyword arguments
    kwargs.setdefault('driver','pytables')
    if (kwargs['driver'].lower() == 'pytables'):
        kwargs.pop('driver')
        # return GeoDataFrame from pytables
        return read_pytables(filename, **kwargs)
    elif (kwargs['driver'].lower() == 'h5py'):
        kwargs.pop('driver')
        # return GeoDataFrame from h5py
        return read_h5py(filename, **kwargs)

# read pandas dataframe from pytables HDF5
def read_pytables(filename, **kwargs):
    # open pytables HDF5 to read pandas dataframe
    df = geopandas.pd.read_hdf(filename, **kwargs)
    # generate geometry column
    geometry = geopandas.points_from_xy(df['longitude'],df['latitude'])
    # build and return GeoDataFrame
    gdf = geopandas.GeoDataFrame(df.drop(columns=['latitude','longitude']),
        geometry=geometry)
    return gdf

# read pandas dataframe from h5py HDF5
def read_h5py(filename, **kwargs):
    # open HDF5 file object
    fileID = h5py.File(filename, mode='r')
    # input dictionary for input variables
    h5 = {}
    # get each variable from HDF5
    for key,val in fileID.items():
        h5[key] = val[:].squeeze()
    # Closing the netCDF file
    fileID.close()
    # Generate Time Column
    delta_time = (h5['delta_time']*1e9).astype('timedelta64[ns]')
    atlas_sdp_epoch = np.datetime64(datetime.datetime(2018, 1, 1))
    h5['time'] = geopandas.pd.to_datetime(atlas_sdp_epoch + delta_time)
    # generate geometry column
    geometry = geopandas.points_from_xy(h5['longitude'], h5['latitude'])
    del h5['longitude']
    del h5['latitude']
    # create Pandas DataFrame object
    df = geopandas.pd.DataFrame(h5)
    # build GeoDataFrame
    gdf = geopandas.GeoDataFrame(df, geometry=geometry)
    # set index
    gdf.set_index('time', inplace=True)
    gdf.sort_index(inplace=True)
    # return geodataframe
    return gdf

# output formats wrapper
def to_file(gdf, filename, format='hdf', **kwargs):
    if format.lower() in ('hdf','hdf5','h5'):
        to_hdf(gdf, filename, **kwargs)
    elif format.lower() in ('netcdf','nc'):
        to_nc(gdf, filename, **kwargs)

# input formats wrapper
def from_file(filename, format='hdf', **kwargs):
    if format.lower() in ('hdf','hdf5','h5'):
        return from_hdf(filename, **kwargs)
    elif format.lower() in ('netcdf','nc'):
        return from_nc(filename, **kwargs)