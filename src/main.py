import numpy as np
from funcs import pixel_to_geo, read_spatial_raster, get_band, segment_image_with_mask
import geopandas as gpd
from shapely.geometry import Polygon
from osgeo import osr
from shapely.ops import transform

raster_file = r"grupa_4.tif"
raster_dataset = read_spatial_raster(raster_file)
raster_projection=raster_dataset.GetProjection()
geo_transform = raster_dataset.GetGeoTransform()
raster_origin = (geo_transform[0], geo_transform[3])  # Top-left
pixel_width = geo_transform[1]
pixel_height = abs(geo_transform[5])  
#print(raster_projection)

coastal_blue = get_band(raster_dataset, 1)
blue = get_band(raster_dataset, 2)
green_i = get_band(raster_dataset, 3)
green = get_band(raster_dataset, 4)
yellow = get_band(raster_dataset, 5)
red = get_band(raster_dataset, 6)
rededge = get_band(raster_dataset, 7)
nir = get_band(raster_dataset, 8)

forest_mask = (red < 300) & (red > 0)   # lasy przyjmują wartości od 0 do 300
forest_mask = np.uint8(forest_mask) 

detected_forests =  segment_image_with_mask(forest_mask, forest_mask)
detected_forests["id"] = np.int64(detected_forests.index)

#wybranie obszarów o powierzchni większej niż 1000 m2 - Zgodnie z art. 3. u.o.l. lasem nazywamy grunt: 
#o zwartej powierzchni co najmniej 0,10 ha, pokryty roślinnością leśną (uprawami leśnymi) 
geometries = geometries = [row["geometry"] for _, row in detected_forests.iterrows()]
geo_geometries = [transform(lambda x, y: pixel_to_geo(geo_transform, x, y), geom) for geom in geometries]
forest_gdf = gpd.GeoDataFrame({'geometry': geo_geometries})
spatial_ref = osr.SpatialReference()
spatial_ref.ImportFromWkt(raster_projection)
forest_gdf.crs = spatial_ref.ExportToProj4()
forest_gdf["area"] = forest_gdf["geometry"].area
forest_gdf = forest_gdf[forest_gdf["area"] > 1000].copy()
forest_gdf.to_file("shp/detected_forests.shp", driver="ESRI Shapefile")

holes = []
for idx, row in forest_gdf.iterrows():
    geometry = row["geometry"]
    for hole in geometry.interiors:
        polygon_hole = Polygon(hole)
        area = Polygon(hole).area
        holes.append({"geometry": polygon_hole, "area": area})
        
          
holes_gdf = gpd.GeoDataFrame(holes)
spatial_ref = osr.SpatialReference()
spatial_ref.ImportFromWkt(raster_projection)
holes_gdf.crs = spatial_ref.ExportToProj4()
holes_gdf = holes_gdf[holes_gdf["area"] > 100].copy() #wybranie dziur o powierzchni większej niż 100 m2
holes_gdf.to_file("shp/forest_holes.shp", driver="ESRI Shapefile")

