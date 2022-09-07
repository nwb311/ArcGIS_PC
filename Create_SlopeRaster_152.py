####################################################################################################
# Program: script to create slope raster for buffer polygon around point dataset
# Author: Abhishek Zeley
# Date: Nov 21, 2021
# Last modified: Nov 21, 2021
####################################################################################################

import arcpy, os                                # import modules
from arcpy import env                           # import env class
from arcpy.sa import *                          # import all from arcpy.sa
env.overwriteOutput = True                      # overwrite output when rerunning the script

elevation = r"C:\Users\nwb31\Desktop\PA3\PA15\Data\dem30"           # variable for input DEM file
pointMask = r"C:\Users\nwb31\Desktop\PA3\PA15\Data\testpoints.shp"  # variable for point feature class
svGoodslpe = r"C:\Users\nwb31\Desktop\PA3\PA15\Data\goodslopeAZ"    # variable for output

env.workspace = os.path.dirname(elevation)                          # specify workspace
inputElev = os.path.basename(elevation)                             # variable to store name of input raster

mask = 'in_memory/Buffers'                                # variable for temporary in memory feature class
arcpy.Buffer_analysis(pointMask, mask, "1000 Meters")     # create Buffer around point feature class

outMeasure = "DEGREE"
zFactor = 0.3048
temp01 = Slope(inputElev, outMeasure, zFactor)            # create slope raster
temp02 = ExtractByMask(temp01, mask)                      # extract area within the buffered area

outRaster = temp02 < 5                                    # extract good slope from selected area
outRaster.save(svGoodslpe)                                # save the temporary raster on disk

del temp01, temp02                                        # delete temporary raster, layer
