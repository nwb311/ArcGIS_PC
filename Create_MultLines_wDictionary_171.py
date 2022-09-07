###################################################################################################
# Program: script to utilize Dictionary to Create Multiple Lines Features
# Author: Abhishek Zeley
# Date: Nov 30, 2021
# Last modified: Nov 30, 2021
####################################################################################################

import arcpy, os                            # import modules
arcpy.env.overwriteOutput = True            # overwrite output when rerunning the script


# ----- take user inputs -----
# gpsFile = r"C:\Users\nwb31\Desktop\PA3\PA17\Data\Reindeer.csv"
# outFC = r"C:\Users\nwb31\Desktop\PA3\PA17\Data\Reindeer.shp"
# coordsys = r"C:\Users\nwb31\Desktop\PA3\PA17\Data\WGS 1984.prj"

gpsFile = arcpy.GetParameterAsText(0)              # take user input for gps track file
outFC = arcpy.GetParameterAsText(1)                # take user input for output feature class name
coordsys = arcpy.GetParameterAsText(2)             # take user input for out FC coordinate system


# ----- specify workspace, create new FC and add new field in it -----
arcpy.env.workspace = os.path.dirname(outFC)        # specify workspace
featClass = os.path.basename(outFC)                 # variable to store outFC

# if arcpy.Exists(featClass):                         # check if FC exist, if yes, then delete FC
#     arcpy.DeleteFeatures_management(featClass)

arcpy.CreateFeatureclass_management(
    arcpy.env.workspace, featClass, "POLYLINE", "", "", "", coordsys)   # create new line FC for reindeer path

arcpy.AddField_management(featClass, "Reindeer", "text", "", "", "20")  # add new field text to store reindeer name


# ----- read gps track (csv) file and extract index positions of desired fields -----
reindeerTrack = open(gpsFile, 'r')                  # open csv file
headerLine = reindeerTrack.readline()               # read first line i.e. header line
lstValue = headerLine.split(",")                    # split line per the specified delimiter

xCoordIndex = lstValue.index("Longitude")           # extract index of specified field
yCoordIndex = lstValue.index("Latitude")            # extract index of specified field
nameIndex = lstValue.index("Reindeer")              # extract index of specified field

lines = reindeerTrack.readlines()                   # read rest of the lines from csv file
reindeerTrack.close()                               # close file


# ----- create dictionary, insert cursor, add point data in dictionary, create line FC from dictionary -----
reindeerDictionary = {}                             # define empty dictionary
fieldList = ["ID", "Reindeer", "SHAPE@"]            # list of fields to be accessed by insert cursor
with arcpy.da.InsertCursor(featClass, fieldList) as isCursor:   # create insert cursor
    for line in lines:                              # iterate through each line from the csv file
        segment = line.split(",")                   # split line per the specified delimiter
        key = segment[nameIndex]                    # variable to store reindeer name

        if key not in reindeerDictionary:                   # check if reindeer name exist in dictionary
            reindeerDictionary[key] = arcpy.Array()         # add new item to dictionary as current reindeer's name
            # print("Add {0} into the record.".format(key))
            arcpy.AddMessage("Add {0} into the record.".format(key))  # print confirmation message
        xCoord = segment[xCoordIndex]                                   # variable to store longitude
        yCoord = segment[yCoordIndex]                                   # variable to store latitude
        reindeerDictionary[key].add(arcpy.Point(xCoord, yCoord))        # create new point and add to dictionary
        # print("Add a point into {0} track.".format(key))
        arcpy.AddMessage("Add a point into {0} track.".format(key))   # print confirmation message

    lid = 0                                                     # define counting variable
    for key in reindeerDictionary:                              # loop through each value (key) in dictionary
        lid += 1                                                # increment counting variable
        newLine = arcpy.Polyline(reindeerDictionary[key])       # create new line feature for each value in dictionary
        isCursor.insertRow([lid, key, newLine])                 # insert new line feature for each value in dictionary


# ----- delete dictionary and cursor -----
reindeerDictionary.clear()
del isCursor
