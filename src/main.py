#import arcpy
import matplotlib.pyplot as plt
import numpy as np
#import rasterio
from funcs import read_spatial_raster, segment_image_with_mask, get_band



raster_file = r"grupa_4.tif"
raster_dataset = read_spatial_raster(raster_file)

coastal_blue = get_band(raster_dataset, 1)
blue = get_band(raster_dataset, 2)
green_i = get_band(raster_dataset, 3)
green = get_band(raster_dataset, 4)
yellow = get_band(raster_dataset, 5)
red = get_band(raster_dataset, 6)
rededge = get_band(raster_dataset, 7)
nir = get_band(raster_dataset, 8)

#wyszukanie obszarów z drzewami
# red_array[(red_array > 300)] = 0
# red_array[np.isnan(red_array)] = 0
# plt.imshow(red_array, cmap='RdYlGn')
# plt.show()

forest_mask = (red < 300) & (red > 0)
forest_mask = np.flipud(forest_mask)
forest_mask = np.uint8(forest_mask)

detected_forests =  segment_image_with_mask(forest_mask, forest_mask)
print(f"number of detected forests: {len(detected_forests)}")

big_forests = detected_forests[detected_forests["geometry"].area > 1000].copy()
big_forests["id"] = np.int64(big_forests.index)
print(f"number of detected forests with area > 1000: {len(big_forests)}")
big_forests.plot(column="id",color="red")
plt.savefig("big_forests.png")
plt.show()

big_forests.set_crs(epsg=32634, inplace=True)
big_forests.to_file("big_forests.shp", driver="ESRI Shapefile") #ląduje w afryce