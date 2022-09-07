###################################################################################################
# Program: script to calculate NDVI from Landsat 7 image
# Author: Abhishek Zeley
# Date: Dec 02, 2021
# Last modified: Dec 02, 2021
####################################################################################################

# ----- import modules -----
import arcpy, os
from arcpy import env
from arcpy.sa import *
env.overwriteOutput = True      # overwrite output when rerunning the script

# ----- take Landsat 7 image as input and define reclassification table -----
image = r"C:\Users\nwb31\Desktop\PA3\PA16\Data\tm020708.img"
remap = RemapRange([[0.3, 1, 1], [0.1, 0.3, 2],
                    [-0.1, 0.1, 3], [-0.3, -0.1, 4], [-1, -0.3, 5]])

env.workspace = os.path.dirname(image)      # specify workspace

baseName = os.path.basename(image)[0:-4]    # retrieve base name of ETM+ image without the extension
saveNDVI = env.workspace + os.sep + "NDVI" + baseName[2:]   # specify output NDVI raster name
saveReclass = saveNDVI + "cls"                              # specify reclassified NDVI raster name
scratchName = "xxextract"                                   # name temporary folder in workspace
arcpy.CreateFolder_management(env.workspace, scratchName)   # create temporary folder in workspace

# ----- Convert multi-bands image into Esri Grid format into the temporary folder -----
extractWs = env.workspace + os.sep + scratchName                # assign temporary workspace name to a variable
arcpy.RasterToOtherFormat_conversion(image, extractWs, "GRID")  # convert single image into image for each band

band4 = extractWs + os.sep + baseName + "c4"                    # save output raster for band 4
band3 = extractWs + os.sep + baseName + "c3"                    # save output raster for band 3
outRaster = Float((Raster(band4) - Raster(band3))) \
                    / Float((Raster(band4) + Raster(band3)))    # calculate NDVI
outRaster.save(saveNDVI)                                        # save NDVI raster as permanent raster

outReclass = Reclassify(outRaster, "VALUE", remap, "NODATA")    # Reclassify raster based on reclassify range table
outReclass.save(saveReclass)                                    # save reclassified NDVI raster as permanent raster

arcpy.Delete_management(extractWs)                              # delete temp folder and individual band rasters
