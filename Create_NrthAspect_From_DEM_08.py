####################################################################################################
# Program: script to find north facing aspect from DEM
# Author: Abhishek Zeley
# Date: Nov 21, 2021
# Last modified: Nov 21, 2021
####################################################################################################

import arcpy, os                                        # import modules
arcpy.env.overwriteOutput = True                        # overwrite output when rerunning the script


# ----- user input for input elevation raster and output north aspect raster  -----

elevation = arcpy.GetParameterAsText(0)                 # variable for input DEM file
svNaspect = arcpy.GetParameterAsText(1)                 # variable for output raster

# elevation = r"C:\Data\dem30"                          # variable for input DEM file
# svNaspect = r"C:\Data\svNaspect"                      # variable for output raster

arcpy.env.workspace = os.path.dirname(elevation)        # specify workspace
inputElev = os.path.basename(elevation)                 # variable to store name of input raster


# ----- calculate aspect values from input rater -----
tempAspect = arcpy.sa.Aspect(inputElev)                 # create aspect raster from input elevation


# ----- values for two north facing aspect ranges -----
minR1 = 0                                               # minimum value for range1 (0 - 22.5 degree)
maxR1 = 22.5                                            # maximum value for range1 (0 - 22.5 degree)

minR2 = 337.5                                           # minimum value for range2 (337.5 - 360 degree)
maxR2 = 360                                             # maximum value for range2 (337.5 - 360 degree)


# ------ map algebra expressions to find cells with value within min-max aspect criteria ------

minRange1 = tempAspect > minR1                         # find cells with aspect >  0
maxRange1 = tempAspect < maxR1                         # find cells with aspect < 22.5

minRange2 = tempAspect > minR2                         # find cells with aspect > 337.5
maxRange2 = tempAspect < maxR2                         # find cells with aspect < 360


# Map algebra Boolean AND/OR expressions to set cell value as 1 if both cells in both raster have value 1, \
#       otherwise set cell value to 0 in the out raster

outRaster1 = minRange1 & maxRange1                      # find cells with aspect value in range1 (0 - 22.5 degree)
outRaster2 = minRange2 & maxRange2                      # find cells with aspect value in range2 (337.5 - 360 degree)

nAspect = outRaster1 | outRaster2                       # find cells with aspect values in range1 OR range2


# use Reclassify function to reclassify outRaster values based on remap table and assign NODATA to missing cell values

remap = arcpy.sa.RemapValue([[0, "NODATA"], [1, 1]])                    # table to remap values

nAspReclasfy = arcpy.sa.Reclassify(nAspect, "Value", remap, "NODATA")   # reclassify values per remap table

nAspReclasfy.save(svNaspect)                                            # save temp reclassified raster to disk


# ----- delete temporary raster -----
del tempAspect, minRange1, maxRange1, minRange2, maxRange2, outRaster1, outRaster2
