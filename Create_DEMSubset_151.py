##################################################################################################
# Program: script to create subset of DEM based on min and max elevation values
# Author: Abhishek Zeley
# Date: Nov 21, 2021
# Last modified: Nov 21, 2021
##################################################################################################

import arcpy, os                              # import modules
arcpy.env.overwriteOutput = True              # overwrite output when rerunning the script


class LicenseError (Exception):               # declare a class to handle license error
    pass


try:
    if arcpy.CheckExtension("Spatial") == "Available":     # check if license for Spatial Analyst extension is available
        arcpy.CheckOutExtension("Spatial")                 # if yes, then check out license

        elevation = r"C:\Users\nwb31\Desktop\PA3\PA15\Data\dem30"   # variable for input DEM file
        inMin = 1000                                                # criteria for minimum elevation value
        inMax = 1100                                                # criteria for maximum elevation value

        arcpy.env.workspace = os.path.dirname(elevation)            # specify workspace
        inputElev = os.path.basename(elevation)                     # variable to store name of input raster
        saveReclass = arcpy.env.workspace + os.sep + inputElev + "Zones"   # variable to save output raster

        # map algebra expressions to find cells with value > min criteria and < max criteria
        minRaster = arcpy.sa.Raster(inputElev) > inMin
        maxRaster = arcpy.sa.Raster(inputElev) < inMax

        # Map algebra Boolean AND expression to set cell value as 1 if both cells in both raster have value 1, \
        #       otherwise set cell value to 0 in the out raster
        outRaster = minRaster & maxRaster

        remap = arcpy.sa.RemapValue([[0, "NODATA"], [1, 1]])        # table to remap values

        # use Reclassify function to reclassify values in the outRaster based on remap table and assign NODATA to \
        #       missing/unknown cell values
        outReclassify = arcpy.sa.Reclassify(outRaster, "Value", remap, "NODATA")

        outReclassify.save(saveReclass)                             # save the in memory raster to a raster on disk

        arcpy.CheckExtension("Spatial")                             # return Spatial Analysts license
    else:
        raise LicenseError                                          # license error handling

# print suitable message if license is unavailable
except LicenseError:
    print("Spatial Analyst license is unavailable.")
except arcpy.ExecuteError:
    print(arcpy.GetMessage(2))
