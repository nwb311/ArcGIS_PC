###################################################################################################
# Program: script to create a single line with GPS track text file
# Author: Abhishek Zeley
# Date: Nov 17, 2021
# Last modified: Nov 18, 2021
####################################################################################################

import arcpy, os                            # import modules
arcpy.env.overwriteOutput = True            # overwrite output when rerunning the script

template = arcpy.GetParameterAsText(0)      # take user input for feature class to be used as template for the output FC
outFC = arcpy.GetParameterAsText(1)         # take user input for output FC path and name
gpsFile = arcpy.GetParameterAsText(2)       # take user input for file with coordinates of points to create the line
coordsys = arcpy.GetParameterAsText(3)      # take user input for coordinate system of the output FC

# template = r"C:\Users\nwb31\Desktop\PA3\PA13\Data\ShapeFiles\gpsTrack.shp"
# outFC = r"C:\Users\nwb31\Desktop\PA3\PA13\Data\ShapeFiles\TrackEvas.shp"
# gpsFile = r"C:\Users\nwb31\Desktop\PA3\PA13\Data\TextFiles\track.txt"
# coordsys = r"C:\Users\nwb31\Desktop\PA3\PA13\Data\ShapeFiles\WGS 1984 UTM Zone 15N.prj"

arcpy.env.workspace = os.path.dirname(outFC)    # specify workspace
featClass = os.path.basename(outFC)             # variable to store name of output FC

# if arcpy.Exists(featClass):
#     arcpy.Delete_management(featClass)

# create new output feature class to store the polyline
arcpy.CreateFeatureclass_management(arcpy.env.workspace, featClass, "POLYLINE", template)

# define coordinate system of the output feature class
arcpy.DefineProjection_management(featClass, coordsys)

# initialize required variables
gpsTrack = open(gpsFile, "r")               # open the file with gps coordinates for points
headerLine = gpsTrack.readline()            # extract the first line which header line from the gps file
lstValue = headerLine.split(",")            # split headerline per the delimiter and store as list
yCoordIndex = lstValue.index("y_proj")      # retrieve index value of y coordinate in the list
xCoordIndex = lstValue.index("x_proj")      # retrieve index value of x coordinate in the list
lines = gpsTrack.readlines()                # read the rest of the text file as a list
gpsTrack.close()                            # close gps coordinates text file

lineArray = arcpy.Array()                   # create an empty array object to store each vertex of polyline
lid = 1                                     # counting variable for feature ID

# create an insert cursor with geometry access and needed attribute field
with arcpy.da.InsertCursor(featClass, ["ID", "Shape@"]) as isCursor:
    for line in lines:                          # loop through each line of the gps text file
        segment = line.split(",")               # split line per the delimiter and store as list
        yCoord = segment[yCoordIndex]           # retrieve value stored at the index position
        xCoord = segment[xCoordIndex]           # retrieve value stored at the index position
        lineArray.add(arcpy.Point(xCoord, yCoord))  # create and add the point object into array for polyline

    isCursor.insertRow([lid, arcpy.Polyline(lineArray)])        # create a new line object with the array
    arcpy.AddMessage("Record number {0} written to feature class.".format(lid))  # print confirmation message
    # print("Record number {0} written to feature class.".format(lid))

# delete cursor and array for line
lineArray.removeAll()
del isCursor
