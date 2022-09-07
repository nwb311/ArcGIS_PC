###################################################################################################
# Program: script to calculate soil wetness index values
# Author: Abhishek Zeley
# Date: Dec 02, 2021
# Last modified: Dec 02, 2021
####################################################################################################

# ----- import modules -----
import arcpy, os
from arcpy import env
from arcpy.sa import *
env.overwriteOutput = True      # overwrite output when rerunning the script

# ----- take elevation raster as input and define variable for output raster -----
elevation = r"C:\Users\nwb31\Desktop\PA3\PA16\Data\dem30"
saveWetindex = r"C:\Users\nwb31\Desktop\PA3\PA16\Data\Wetindex"

env.workspace = os.path.dirname(elevation)                  # specify workspace
inputElev = os.path.basename(elevation)                     # retrieve elevation raster name

# ----- calculate slope, flow accumulation and wetness index -----
outSlope = Slope(inputElev, "PERCENT_RISE", 0.3048)         # create slope raster
outFlowacc = FlowAccumulation(FlowDirection(inputElev))     # calculate catchment area using nested functions
outWetindex = Ln((outFlowacc * 900) / Tan(outSlope))        # calculate soil wetness index


# ----- smooth out the wetness index values using neighborhood mean -----
neighborhood = NbrRectangle(3, 3, "CELL")                   # create neighborhood object for 3x3 rectangle neighborhood
meanWetindex = FocalStatistics(outWetindex, neighborhood, "MEAN")  # smooth the wetness index values using neigbrhd mean
meanWetindex.save(saveWetindex)                             # save raster object as permanent

del outSlope, outFlowacc, outWetindex                       # delete temporary raster
