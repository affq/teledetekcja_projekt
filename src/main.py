#import arcpy
import matplotlib.pyplot as plt
import numpy as np
#import rasterio
from funcs import read_spatial_raster, segment_image_with_mask, get_band, reproject_geodataframe, convert_to_pixel_system
import geopandas as gpd
from shapely.geometry import Polygon



raster_file = r"grupa_4.tif"
raster_dataset = read_spatial_raster(raster_file)
raster_projection=raster_dataset.GetProjection()
#print(raster_projection)

coastal_blue = get_band(raster_dataset, 1)
blue = get_band(raster_dataset, 2)
green_i = get_band(raster_dataset, 3)
green = get_band(raster_dataset, 4)
yellow = get_band(raster_dataset, 5)
red = get_band(raster_dataset, 6)
rededge = get_band(raster_dataset, 7)
nir = get_band(raster_dataset, 8)

forest_mask = (red < 300) & (red > 0)   #lasy przyjmuja wartosci od 0 do 300
forest_mask = np.uint8(forest_mask)

detected_forests =  segment_image_with_mask(forest_mask, forest_mask)
#print(f"number of detected forests: {len(detected_forests)}")

big_forests = detected_forests[detected_forests["geometry"].area > 1000].copy()
big_forests["id"] = np.int64(big_forests.index)

holes = []
for idx, row in big_forests.iterrows():
    geometry = row["geometry"]
    for hole in geometry.interiors:
        holes.append({"id": row["id"], "geometry": Polygon(hole)})

holes_gdf = gpd.GeoDataFrame(holes)
holes_gdf["area"] = holes_gdf["geometry"].area
# print(f"number of holes: {len(holes_gdf)}")
holes_gdf = holes_gdf[holes_gdf["area"] > 100].copy()
#print(f"number of holes with area > 100: {len(holes_gdf)}")

holes_gdf.crs = raster_projection
holes_features = convert_to_pixel_system(holes_gdf, raster_dataset.GetGeoTransform())
holes_features.to_file("forest_holes.shp", driver="ESRI Shapefile")




