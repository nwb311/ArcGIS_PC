###################################################################################################
# Program: script to parse JSON Response and Create Polygon Features
# Author: Abhishek Zeley
# Date: Dec 01, 2021
# Last modified: Dec 01, 2021
####################################################################################################

import arcpy, os, json                              # import modules
arcpy.env.overwriteOutput = True                    # overwrite output when rerunning the script


# ----- take user inputs -----
# textFile = r"C:\Users\nwb31\Desktop\PA3\PA17\Data\Nodaway.txt"
# outFC = r"C:\Users\nwb31\Desktop\PA3\PA17\Data\Nodaway.shp"

textFile = arcpy.GetParameterAsText(0)             # take user input for JSON text file
outFC = arcpy.GetParameterAsText(1)                # take user input for output feature class name


# ----- specify workspace, create new FC and add new field in it -----
arcpy.env.workspace = os.path.dirname(outFC)        # specify workspace
featClass = os.path.basename(outFC)                 # variable to store outFC

# if arcpy.Exists(featClass):                         # check if FC exist, if yes, then delete FC
#     arcpy.DeleteFeatures_management(featClass)


# ----- read JSON file (text) -----
fileRead = open(textFile, 'r')                      # open text file
fileContents = fileRead.read()                      # read the entire file and store as string in variable
decoded = json.loads(fileContents)  # use load function in JSON module to convert contents into Python Dictionary object
fileRead.close()                                    # close file

geometryType = decoded['geometryType'][12:]         # retrieve geometry type information of feature layer
coordsys = decoded['spatialReference']['wkid']      # retrieve coordinate system information

arcpy.CreateFeatureclass_management(
    arcpy.env.workspace, featClass, geometryType, '', '', '', coordsys)   # create new FC


fieldList = ["ID", "SHAPE@"]            # list of fields to be accessed by insert cursor

for rslt in decoded['fields']:          # loop through each field definition for key 'fields' in JSON file
    if rslt['type'][13:] == 'String':   # check if corresponding value to field 'type' is 'string'
        fieldType = 'text'              # set field type as text
        fieldLength = rslt['length']    # retrieve field length information

    elif rslt['type'][13:] == 'Integer':  # check if corresponding value to field 'type' is 'integer'
        fieldType = 'long'              # set field type as long
        fieldLength = ''                # set field length variable as null

    else:
        fieldType = rslt['type'][13:]   # set field type as retrieved value
        fieldLength = ''                # set field length variable as null

    arcpy.AddField_management(featClass, rslt['name'], fieldType,
                              "", "", fieldLength, rslt['alias'])  # add new field based on info retrieve from JSON file

    fieldList.append(rslt['name'])      # add new field at end of fieldList
# print("The current fields are {0}.".format(fieldList))
arcpy.AddMessage("The current fields are {0}.".format(fieldList))  # print field name verification message

polygonArray = arcpy.Array()            # create empty array to store polygon geometry information
pid = 1                                 # set counting variable to 1

with arcpy.da.InsertCursor(featClass, fieldList) as isCursor:   # create insert cursor
    for rslt in decoded['features']:                            # iterate through each value of the key 'features'
        for coordPair in rslt['geometry']['rings'][0]:
            xCoord = coordPair[0]                               # variable to store longitude
            yCoord = coordPair[1]                               # variable to store latitude
            polygonArray.add(arcpy.Point(xCoord, yCoord))       # create new point and add to array
        newPolygon = [pid, arcpy.Polygon(polygonArray)]         # create new array and add pid and polygon array in it

        for fld in fieldList:
            if fld == "ID" or fld == "SHAPE@":
                continue
            newPolygon.append(rslt['attributes'][fld])  # if field name is not ID or Shape then add field to end of list

        isCursor.insertRow(newPolygon)                      # use insert cursor to create new polygon feature
        # print("Add Polygon {0}.".format(pid))
        arcpy.AddMessage("Add Polygon {0}.".format(pid))    # print verification message
        pid += 1                                            # increment counting variable
        polygonArray.removeAll()                            # clean upu array


# ----- delete cursor -----
del isCursor
