from osgeo import gdal
gdal.UseExceptions()
from typing import Union
from pathlib import Path
import shapely
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
from rasterio.features import shapes
import geopandas as gpd

def show_grayscale_matplotlib(array: np.ndarray):  
    plt.imshow(array, cmap='gray')

def read_spatial_raster(path: Union[str, Path]) -> gdal.Dataset:
    dataset = gdal.Open(str(path))
    assert dataset is not None, "Read spatial raster returned None"
    return dataset

def points_to_pixels(points: np.ndarray, geotransform) -> np.ndarray:
    c, a, _, f, _, e = geotransform
    columns = (points[:, 0] - c) / a
    rows = (points[:, 1] - f) / e
    pixels = np.vstack([rows, columns])
    pixels = pixels.T
    return pixels

def reproject_geodataframe(features: gpd.GeoDataFrame, crs: str) -> gpd.GeoDataFrame:
    return features.to_crs(crs)

def convert_to_pixel_system(features: gpd.GeoDataFrame, geotransform) -> gpd.GeoDataFrame:
    def transform_function(xy: np.ndarray):
        ij = points_to_pixels(xy, geotransform)
        ji = ij[:, [1, 0]]
        return ji
    
    
    indices = features.index
    for i in indices:
        geometry = features.loc[i, "geometry"]
        geometry = shapely.transform(geometry, transform_function)
        features.loc[i, "geometry"] = geometry
    return features

def point_to_pixel(x, y, geotransform):
    c, a, b, f, d, e = geotransform
    column = (x - c) / a
    row = (y - f) / e
    return row, column  # ij convention to stay with NumPy

def segment_image_with_mask(image: np.ndarray, include_mask:np.ndarray):
    shapes_from_image = shapes(image, include_mask)
    shapes_from_image = [{'properties': {'raster_val': v}, 'geometry':s} for s,v in shapes_from_image]
    shapes_from_image =gpd.GeoDataFrame.from_features(shapes_from_image)
    return shapes_from_image

def get_band(raster_dataset, band_number: int):
    band = raster_dataset.GetRasterBand(band_number)
    band_array = band.ReadAsArray()
    band_array = np.copy(band_array)
    band_array = np.float32(band_array)
    return band_array

def pixel_to_geo(transform, x, y):
    """
    Convert pixel coordinates to geographic coordinates.
    
    Parameters:
    - transform: GeoTransform of the raster (tuple)
    - x: Pixel column (int)
    - y: Pixel row (int)
    
    Returns:
    - (geoX, geoY): Geographic coordinates
    """
    geoX = transform[0] + x * transform[1] + y * transform[2]
    geoY = transform[3] + x * transform[4] + y * transform[5]
    return geoX, geoY

def reproject_geometry(geometry, transform):
    """
    Reproject a geometry from pixel to geographic coordinates.
    """
    def pixel_to_geo_transform(x, y):
        return pixel_to_geo(transform, x, y)

    return transform(geometry, pixel_to_geo_transform)