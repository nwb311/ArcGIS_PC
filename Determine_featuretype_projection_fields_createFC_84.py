###################################################################################################
# Program: Determine feature type, projection, fields and use feature class as template to create new feature classes
# Author: Abhishek Zeley
# Date: Nov 4, 2021
# Last modified: Nov 4, 2021
# Description:  write script to determine feature type, fields of feature classes in the current workspace,
#               create new feature class based on template feature class

# Variables:
#   fc:         store feature class
#   desc:       description of feature class
#   shapeType:  geometry of feature class
#   fieldList:  list of fields in feature class
#   spatialRef: store spatial reference from description
#   outputWS:   store output workspace
#   outfc:      store output feature class
#   template:   store path of feature class used as template
#   outCS:      coordinate system of feature class used as template
#   year:       store year from range for iteration of for loop
#   newfile:    store new file name

###################################################################################################

import arcpy, os                # import arcpy and os modules

arcpy.env.workspace = r"C:\Users\nwb31\Desktop\PA3\PA8_Data\Data"  # specify workspace
arcpy.env.overwriteOutput = True    # enable overwrite output when re-running the script

fc = "precip.shp"                                              # initialize variable to store shape file
desc = arcpy.Describe(fc)                                      # store description of shape file

shapeType = desc.ShapeType                                     # store shape type from description of shape file
print("The geometry of {0} is {1}.".format(fc, shapeType))     # print file name and it's shape type


# create a list of fields
fieldList = arcpy.ListFields(fc)

# for loop to print information of each field in the shape file
for field in fieldList:
    print("{0} is a type of {1} with a length of {2}."
          .format(field.name, field.type, field.length))

# store and print spatial reference from description of shape file
spatialRef = desc.SpatialReference
print("The coordinate system of {0} is {1}.".format(fc, spatialRef.name))


outputWS = os.path.join(arcpy.env.workspace, "Missouri.gdb")        # specify output workspace
outfc = outputWS + os.sep + fc[:-4] + "2002"                        # define output feature class and specify it's path

template = os.path.join(outputWS, "MOBoundary")                     # define feature class to be used as template
outCS = arcpy.Describe(template).spatialReference                   # obtain spatial reference of template
arcpy.Project_management(fc, outfc, outCS)    # use project tool in Data Management toolbox to project the feature class
print("{0} is projected to {1}.".format(fc, outCS.Name))            # print feature class is projected as per template

# for loop to create empty feature classes for years 2003-2006 using feature class created above as template
for year in range(2003, 2006):
    newfile = fc[:-4] + str(year)                                   # variable for feature class name
    arcpy.CreateFeatureclass_management(outputWS, newfile, shapeType, outfc)    # create feature class
    print("Create Feature Class {0} in {1}.".format(newfile, outputWS))  # print message for newly created feature class
