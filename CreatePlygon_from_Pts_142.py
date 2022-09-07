###################################################################################################
# Program: script to create polygon feature class
# Author: Abhishek Zeley
# Date: Nov 18, 2021
# Last modified: Nov 18, 2021
####################################################################################################

import arcpy, os                            # import modules
arcpy.env.overwriteOutput = True            # overwrite output when rerunning the script

outFC = arcpy.GetParameterAsText(0)         # take user input for output FC path and name
inFile = arcpy.GetParameterAsText(1)        # take user input for file with coordinates of points to create the polygon
coordsys = arcpy.GetParameterAsText(2)      # take user input for coordinate system of the output FC

# outFC = r"C:\Users\nwb31\Desktop\PA3\PA14\Data\ShapeFiles\UnknownPolygon.shp"
# inFile = r"C:\Users\nwb31\Desktop\PA3\PA14\Data\TextFiles\UnknownPolygon.txt"
# coordsys = r"C:\Users\nwb31\Desktop\PA3\PA14\Data\ShapeFiles\WGS 1984.prj"

arcpy.env.workspace = os.path.dirname(outFC)    # specify workspace
featClass = os.path.basename(outFC)             # variable to store name of output FC

# if arcpy.Exists(featClass):
#     arcpy.Delete_management(featClass)

# create new output feature class to store the polyline
arcpy.CreateFeatureclass_management(arcpy.env.workspace, featClass, "POLYGON")

# define coordinate system of the output feature class
arcpy.DefineProjection_management(featClass, coordsys)

# initialize required variables
pntFile = open(inFile, "r")                 # open the file with gps coordinates for points
line = pntFile.readline()                   # extract the line from the text file
pntFile.close()                             # close gps coordinates text file
coordPairs = line.split("|")                # split line per the delimiter and store as list

polygonArray = arcpy.Array()                # create an empty array object to store each vertex of polygon
pid = 0                                     # counting variable for feature ID

# create an insert cursor with geometry access and needed attribute field
with arcpy.da.InsertCursor(featClass, ["SHAPE@"]) as isCursor:
    for coordinates in coordPairs:                      # loop through each coordinate pair
        coord = coordinates.split(",")                  # split line per the delimiter and store as list
        xCoord = coord[0]                               # retrieve value stored at the index position
        yCoord = coord[1]                               # retrieve value stored at the index position
        polygonArray.add(arcpy.Point(xCoord, yCoord))   # create and add the point object into array for polygon
        pid += 1                                        # increment counting variable
        arcpy.AddMessage("Add {0} point".format(pid))   # print confirmation message
        # print("Add {0} point".format(pid))            # print confirmation message

    endX = coordPairs[0].split(",")[0]                  # retrieve value for first point stored at the index position
    endY = coordPairs[0].split(",")[1]                  # retrieve value for first point stored at the index position
    polygonArray.add(arcpy.Point(endX, endY))           # create and add the point object into array for polygon
    pid += 1                                            # increment counting variable
    arcpy.AddMessage("Add (0) point".format(pid))       # print confirmation message
    # print("Add (0) point".format(pid))                # print confirmation message
    newPolygon = arcpy.Polygon(polygonArray)            # create new polygon object with the array
    isCursor.insertRow([newPolygon])                    # insert a new feature in the feature class with the array

# delete cursor and array for line
polygonArray.removeAll()
del isCursor
