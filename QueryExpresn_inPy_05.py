###################################################################################################
# Program: script to construct query expression for ArcGIS data with Python
# Author: Abhishek Zeley
# Date: Nov 14, 2021
# Last modified: Nov 14, 2021
####################################################################################################

import arcpy                                                            # import module

arcpy.env.workspace = r"C:\Users\nwb31\Desktop\PA3\lab05\Data_New"      # define workspace
arcpy.env.overwriteOutput = True                                        # enable overwrite output

# -------- Find rivers in Mississippi River system --------

# define variable to store feature class and feature layer
rivers_feat = "rivers.shp"
riv_layer = "Rivers"

if arcpy.Exists(riv_layer):                                  # check if feature layer exists
    arcpy.Delete_management(riv_layer)                       # if yes, then delete feature layer

query = '"SYSTEM" = \'Mississippi\''                         # build query to select rivers with Mississippi as SYSTEM
arcpy.MakeFeatureLayer_management(rivers_feat, riv_layer, query)  # create feature layer for feature class per the query


# -------- Copy rivers in Mississippi River system into new shape file --------

out_feat = "MRS.shp"                                        # define variable to store feature class
if arcpy.Exists(out_feat):                                  # check if feature class exists
    arcpy.Delete_management(out_feat)                       # if yes, then delete feature class
arcpy.CopyFeatures_management(riv_layer, out_feat)          # copy feature layer to new feature class


# -------- # Select states that intersect with rivers in Mississippi River system --------

# define variable to store feature class and feature layer
states_feat = "States.shp"
st_layer = "States"

arcpy.MakeFeatureLayer_management(states_feat, st_layer)        # create feature layer for feature class

arcpy.SelectLayerByLocation_management(st_layer, "INTERSECT", out_feat)     # use select by location with intersect

# count and print number of features
result = arcpy.GetCount_management(st_layer)
print("There are {0} states in Mississippi River system.".format(result))


# -------- Copy states that intersect with rivers in Mississippi River system into a new shape file --------

# define variable to store feature class
sel_feat = "Mississippi.shp"

if arcpy.Exists(sel_feat):                                  # check if feature layer exists
    arcpy.Delete_management(sel_feat)                       # if yes, then delete feature layer

arcpy.CopyFeatures_management(st_layer, sel_feat)           # copy feature layer to new feature class

print("Copy the feature layer \"{0}\" to feature class \"{1}\".".format(st_layer, sel_feat))


# ---- Use select by attribute on states that intersect with Mississippi River system and have POP2008 > 10,000,000 ----

query = '"POP2008" > 10000000'                                 # build query to select states with POP2008 > 10,000,000

arcpy.MakeFeatureLayer_management(sel_feat, st_layer, query)   # create feature layer for feature class per the query

result = arcpy.GetCount_management(st_layer)                   # count number of features
print("There are {0} states in Mississippi River system with 2008 population greater than 10,000,000.".format(result))


# ------ copy attribute table of states in Mississippi River system with pop2008 > 10,000,000 in a new table -----

out_table = "POPMiss.dbf"                                   # define variable to store new table

if arcpy.Exists(out_table):                                 # check if table exists
    arcpy.Delete_management(out_table)                      # if yes, then delete table

arcpy.CopyRows_management(st_layer, out_table)              # copy attribute table of layer into a new table

print("Copy the attributes of the feature layer \"{0}\" to table \"{1}\".".format(st_layer, out_table))
