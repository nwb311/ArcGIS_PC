###################################################################################################
# Program: script to create points in new Point feature class from a csv file
# Author: Abhishek Zeley
# Date: Nov 20, 2021
# Last modified: Nov 20, 2021
####################################################################################################

import arcpy, os                              # import modules
arcpy.env.overwriteOutput = True              # overwrite output when rerunning the script

outFC = arcpy.GetParameterAsText(0)           # take user input for output FC path and name
textFile = arcpy.GetParameterAsText(1)        # take user input for text file w/coordinates and attributes for points
coordsys = arcpy.GetParameterAsText(2)        # take user input for coordinate system of the output FC

# outFC = r"C:\Users\nwb31\Desktop\PA3\lab07\Data\Shapefiles\DCC.shp"
# textFile = r"C:\Users\nwb31\Desktop\PA3\lab07\Data\TextFiles\crime_incidents_2011_CSV.csv"
# coordsys = r"C:\Users\nwb31\Desktop\PA3\lab07\Data\Shapefiles\NAD 1983.prj"


arcpy.env.workspace = os.path.dirname(outFC)    # specify workspace
featClass = os.path.basename(outFC)             # variable to store name of output FC


# # ----- check if FC exists, if yes, then delete FC -----
# if arcpy.Exists(featClass):
#     arcpy.Delete_management(featClass)


# ----- create new FC to store DC crime Point data -----
arcpy.CreateFeatureclass_management(arcpy.env.workspace, featClass, "Point")


# ----- define coordinate system of the output feature class -----
arcpy.DefineProjection_management(featClass, coordsys)


# ----- add new fields in the newly created FC -----
fldList = ["OFFENSE", "METHOD", "DISTRICT"]
for fld in fldList:
    # valFld = arcpy.ValidateFieldName(fld)
    # arcpy.AddField_management(featClass, valFld, "TEXT", "50")
    arcpy.AddField_management(featClass, fld, "TEXT", "50")


# ----- open text file, read header line and retrieve index values of required fields -----
csvFile = open(textFile, "r")                       # open text file
headerLine = csvFile.readline()                     # read first line which is the header line
spltHeadrLine = headerLine.split(",")               # split the header line per delimiter and store as a list

frstFldIndex = spltHeadrLine.index("OFFENSE")       # retrieve index value for the specified field
scndFldIndex = spltHeadrLine.index("METHOD")        # retrieve index value for the specified field
thrdFldIndex = spltHeadrLine.index("DISTRICT")      # retrieve index value for the specified field
xCoorIndex = spltHeadrLine.index("LONGITUDE")       # retrieve index value for the specified field
yCoorIndex = spltHeadrLine.index("LATITUDE")        # retrieve index value for the specified field

lines = csvFile.readlines()                         # read rest of the lines in the text file
csvFile.close()                                     # close the text file


# ----- create an insert cursor with geometry access and needed attribute field -----
pid = 1                                                           # counting variable for feature ID
fieldList = ["ID", "OFFENSE", "METHOD", "DISTRICT", "Shape@"]     # list of fields that the cursor is allowed to access

with arcpy.da.InsertCursor(featClass, fieldList) as isCursor:     # create insert cursor
    for line in lines:                                            # loop through each line from the text file
        spltLine = line.split(",")                                # split line per delimiter and store as a list

        xCoord = float(spltLine[xCoorIndex])                      # retrieve value for stored at specified index
        yCoord = float(spltLine[yCoorIndex])                      # retrieve value for stored at specified index

        if xCoord == 0 or yCoord == 0:              # if long or lat value in text file is zero then skip to next line
            continue

        frstFld = spltLine[frstFldIndex]                          # retrieve value for stored at specified index
        scndFld = spltLine[scndFldIndex]                          # retrieve value for stored at specified index
        thrdFld = spltLine[thrdFldIndex]                          # retrieve value for stored at specified index

        newPoint = [pid, frstFld, scndFld, thrdFld, arcpy.Point(xCoord, yCoord)]  # fields list to pass to insert cursor

        isCursor.insertRow(newPoint)  # use insert cursor to insert new record in out feature class

        # print("Record number {0} written to feature class.".format(pid))
        pid += 1         # increment counting variable
    pid -= 1             # decrement counting variable by 1 to print the correct value in confirmation message
    arcpy.AddMessage("{0} records have been written into the new feature class.".format(pid))  # print confrmatn message
    # print("{0} records have been written into the new feature class.".format(pid))  # print confirmation message

# ----- delete cursor -----
del isCursor
