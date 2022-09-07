###################################################################################################
# Program: script to retrieve records with a spatial query
# Author: Abhishek Zeley
# Date: Nov 11, 2021
# Last modified: Nov 11, 2021
####################################################################################################

import arcpy        # import module

# define required variables
county = "Ozark"
inputFC = r"C:\Users\nwb31\Desktop\PA3\PA11\Data\MOcnty.shp"
fieldName = "NAME"

# assign file path to workspace
arcpy.env.workspace = arcpy.Describe(inputFC).path

# create feature layer for input feature class
arcpy.MakeFeatureLayer_management(inputFC, "AllCntyLyr")

# build query
query = "\"{0}\" = \'{1}\'".format(fieldName, county)

# create feature layer for input feature class
arcpy.MakeFeatureLayer_management(inputFC, "SelCntyLyr", query)

# use select by location
arcpy.SelectLayerByLocation_management(
    "AllCntyLyr", "BOUNDARY_TOUCHES", "SelCntyLyr")

# print message using tailing comma
print("The neighboring counties of {0} are: ".format(county)),

# use 'with' with cursor creation to avoid data lock
with arcpy.da.SearchCursor("AllCntyLyr", fieldName) as srCursor:
    for row in srCursor:
        if row[0] != county:
            print(row[0]),
    print("\n")

# delete layers and search cursor
arcpy.Delete_management("AllCntyLyr")
arcpy.Delete_management("SelCntyLyr")
del srCursor