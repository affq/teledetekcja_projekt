#import arcpy
import matplotlib.pyplot as plt
import numpy as np
#import rasterio
from funcs import read_spatial_raster, segment_image_with_mask





raster_file = r"grupa_4.tif"
raster_dataset = read_spatial_raster(raster_file)

coastal_blue = raster_dataset.GetRasterBand(1)
coastal_blue_array = coastal_blue.ReadAsArray()
coastal_blue_array = np.copy(coastal_blue_array)

blue = raster_dataset.GetRasterBand(2)
blue_array = blue.ReadAsArray()
blue_array = np.copy(blue_array)

green_i = raster_dataset.GetRasterBand(3)
green_i_array = green_i.ReadAsArray()
green_i_array = np.copy(green_i_array)

green = raster_dataset.GetRasterBand(4)
green_array = green.ReadAsArray()
green_array = np.copy(green_array)

yellow = raster_dataset.GetRasterBand(5)
yellow_array = yellow.ReadAsArray()
yellow_array = np.copy(yellow_array)

red = raster_dataset.GetRasterBand(6)
red_array = red.ReadAsArray()
red_array = np.copy(red_array)

rededge = raster_dataset.GetRasterBand(7)
rededge_array = rededge.ReadAsArray()
rededge_array = np.copy(rededge_array)

nir = raster_dataset.GetRasterBand(8)
nir_array = nir.ReadAsArray()
nir_array = np.copy(nir_array)

coastal_blue_array = np.float32(coastal_blue_array)
blue_array = np.float32(blue_array)
green_i_array = np.float32(green_i_array)
green_array = np.float32(green_array)
yellow_array = np.float32(yellow_array)
red_array = np.float32(red_array)
rededge_array = np.float32(rededge_array)
nir_array =np.float32(nir_array)

#wyszukanie obszarów z drzewami
# red_array[(red_array > 300)] = 0
# red_array[np.isnan(red_array)] = 0
# plt.imshow(red_array, cmap='RdYlGn')
# plt.show()


forest_mask = red_array < 300
forest_mask = np.uint8(forest_mask)

detected_forests =  segment_image_with_mask(forest_mask, forest_mask)
print(f"number of detected forests: {len(detected_forests)}")

big_forests = detected_forests[detected_forests["geometry"].area > 1000].copy()
big_forests["id"] = np.int64(big_forests.index)
print(f"number of detected forests with area > 1000: {len(big_forests)}")
big_forests.plot(column="id",color="red")
plt.savefig("big_forests.png")
plt.show()
