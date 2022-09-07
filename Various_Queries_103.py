###################################################################################################
# Program: script to practice various query expressions
# Author: Abhishek Zeley
# Date: Nov 11, 2021
# Last modified: Nov 11, 2021
###################################################################################################

import arcpy        # import modules

arcpy.env.workspace = r"C:\Users\nwb31\Desktop\PA3\PA10\Data"       # define workspace
arcpy.env.overwriteOutput = True                                    # enable overwrite output

# define variable to store feature class and feature layer
park_feat = "parks.shp"
quake_feat = "quakehis.shp"
river_feat = "rivers.shp"
state_feat = "States.shp"
park_layer = "parks"
quake_layer = "quakes"
river_layer = "rivers"
st_layer = "States"

out_feat = "SelParks.shp"
out_table = "SelState.dbf"

# check if feature layer exists. If yes, then delete feature layer.
if arcpy.Exists(park_layer):
    arcpy.Delete_management(park_layer)

query = '"NAME" LIKE \'%NP%\''      # build query

arcpy.MakeFeatureLayer_management(park_feat, park_layer, query)     # create in memory feature layer for feature class

# count and print number of features
result = arcpy.GetCount_management(park_layer)
print("There are {0} national parks.".format(result))

# check if feature layer exists. If yes, then delete feature layer.
if arcpy.Exists(quake_layer):
    arcpy.Delete_management(quake_layer)

query = '"MAG" >= 5'        # build query

arcpy.MakeFeatureLayer_management(quake_feat, quake_layer, query)     # create in memory feature layer for feature class

# count and print number of features
result = arcpy.GetCount_management(quake_layer)
print("There are {0} earthquake hits with magnitude 5 or higher.".format(result))

# use select by location
arcpy.SelectLayerByLocation_management(park_layer, "WITHIN A DISTANCE", quake_layer, "50 Miles")

# count and print number of features
result = arcpy.GetCount_management(park_layer)
print("There are {0} national parks located within 50 Miles of \
earthquake hits with magnitude 5 or higher.".format(result))

# Pg16
# check if feature layer exists. If yes, then delete feature layer.
if arcpy.Exists(river_layer):
    arcpy.Delete_management(river_layer)

arcpy.MakeFeatureLayer_management(river_feat, river_layer)      # create in memory feature layer for feature class

# use select by location
arcpy.SelectLayerByLocation_management(
    park_layer, "INTERSECT", river_layer)

# count and print number of features
result = arcpy.GetCount_management(park_layer)
print("{0} of these national parks have major rivers crossing \
the park.".format(result))

# check if feature layer exists. If yes, then delete feature layer.
if arcpy.Exists(out_feat):
    arcpy.Delete_management(out_feat)
arcpy.CopyFeatures_management(park_layer, out_feat)     # copy feature
print("Copy the selected features to {0}.".format(out_feat))

# check if feature layer exists. If yes, then delete feature layer.
if arcpy.Exists(st_layer):
    arcpy.Delete_management(st_layer)
arcpy.MakeFeatureLayer_management(state_feat, st_layer)     # create in memory feature layer for feature class

# use select by location
arcpy.SelectLayerByLocation_management(
    st_layer, "INTERSECT", park_layer)

# count and print number of features
result = arcpy.GetCount_management(st_layer)
print("These parks locate within {0} states.".format(result))

# check if feature layer exists. If yes, then delete feature layer.
if arcpy.Exists(out_table):
    arcpy.Delete_management(out_table)
arcpy.CopyRows_management(st_layer, out_table)  # copy selected features into table
print("Copy the selected states into {0}.".format(out_table))

# delete layers
arcpy.Delete_management(park_layer)
arcpy.Delete_management(quake_layer)
arcpy.Delete_management(river_layer)
arcpy.Delete_management(st_layer)
