###################################################################################################
# Program: script to write GPS point data to a feature with an insert cursor
# Author: Abhishek Zeley
# Date: Nov 17, 2021
# Last modified: Nov 17, 2021
####################################################################################################

import arcpy                                     # import modules
arcpy.env.overwriteOutput = True                 # overwrite output when rerunning the script

inputFC = arcpy.GetParameterAsText(0)            # take user input for feature class to write the GPS point features in
gpsFile = arcpy.GetParameterAsText(1)            # take user input for GPS coordinate text file

# inputFC = r"C:\Users\nwb31\Desktop\PA3\PA13\Data\ShapeFiles\gpsWaypoint.shp"
# gpsFile = r"C:\Users\nwb31\Desktop\PA3\PA13\Data\TextFiles\waypoint.txt"

arcpy.env.workspace = arcpy.Describe(inputFC).path      # specify workspace
featClass = arcpy.Describe(inputFC).file                # retrieve name of input feature class

# check if feature class has existing features. If yes, then delete them
if int(arcpy.GetCount_management(inputFC).getOutput(0)) > 0:
    arcpy.DeleteFeatures_management(inputFC)

fileRead = open(gpsFile, 'r')       # open the file with gps coordinates for points
lines = fileRead.readlines()        # # read all lines from the text file as a list
fileRead.close()                    # close gps coordinates text file

pid = 1                                                 # counting variable for feature ID
fieldList = ["ID", "Ident", "Comment", "Shape@"]        # list of fields that the cursor is allowed to access

# create an insert cursor with access to specified fields
with arcpy.da.InsertCursor(featClass, fieldList) as isCursor:
    for line in lines:                      # loop through each line of the gps text file
        if "type" in line:                  # ignore line that contains value as "type" (header line)
            continue

        lstValue = line.split(",")          # split line per the delimiter and store as list
        xCoord = float(lstValue[5])         # retrieve value stored at the index position
        yCoord = float(lstValue[4])         # retrieve value stored at the index position
        ident = str(lstValue[1])            # retrieve value stored at the index position
        comment = str(lstValue[6])          # retrieve value stored at the index position

        newPoint = [pid, ident, comment, arcpy.Point(xCoord, yCoord)]
        isCursor.insertRow(newPoint)        # user insert cursor to insert new record in feature class
        arcpy.AddMessage("Record number {0} written to feature class.".format(pid))  # print confirmation message
        # print("Record number {0} written to feature class.".format(pid))
        pid = pid +1                        # increment counting variable

arcpy.AddMessage("Point Shapefile complete.")   # print completion message
# print("Point Shapefile complete.")
del isCursor                                # delete cursor
