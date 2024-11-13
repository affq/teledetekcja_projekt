import arcpy
import matplotlib.pyplot as plt
import numpy as np
from funcs import read_spatial_raster

raster_file = r"grupa_4.tif"
raster_dataset = read_spatial_raster(raster_file)

coastal_blue = raster_dataset.GetRasterBand(1)
coastal_blue_array = coastal_blue.ReadAsArray()
coastal_blue_array = np.copy(coastal_blue)

blue = raster_dataset.GetRasterBand(2)
blue_array = blue.ReadAsArray()
blue_array = np.copy(blue)

green_i = raster_dataset.GetRasterBand(3)
green_i_array = green_i.ReadAsArray()
green_i_array = np.copy(green_i)

green = raster_dataset.GetRasterBand(4)
green_array = green.ReadAsArray()
green_array = np.copy(green)

yellow = raster_dataset.GetRasterBand(5)
yellow_array = yellow.ReadAsArray()
yellow_array = np.copy(yellow)

red = raster_dataset.GetRasterBand(6)
red_array = red.ReadAsArray()
red_array = np.copy(red)

rededge = raster_dataset.GetRasterBand(7)
rededge_array = rededge.ReadAsArray()
rededge_array = np.copy(rededge)

nir = raster_dataset.GetRasterBand(8)
nir_array = nir.ReadAsArray()
nir_array = np.copy(nir)