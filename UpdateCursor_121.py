###################################################################################################
# Program: script to update records with the update cursor
# Author: Abhishek Zeley
# Date: Nov 13, 2021
# Last modified: Nov 13, 2021
####################################################################################################

import arcpy                # import module

inputFC = r"C:\Users\nwb31\Desktop\PA3\PA12\Data\MOHigherEd.shp"        # variable to store shapefile
fieldNew = "FullAddr"                                                   # variable to store new field name
fieldList = ["Address", "City", "State", "ZIP", fieldNew]     # variable for list of field to be accessed through cursor

arcpy.env.workspace = arcpy.Describe(inputFC).path                      # specify workspace

feat_Class = arcpy.Describe(inputFC).file                               # variable to store file name

fieldNew = arcpy.ValidateFieldName(fieldNew)     # function to validate if field name is valid per ArcGIS requirements

fields = arcpy.ListFields(feat_Class, fieldNew)     # store list of field names in the file

# loop to check if new field name already exist in attribute table and if yes, then delete existing field
for fld in fields:
    arcpy.DeleteField_management(feat_Class, fieldNew)

arcpy.AddField_management(feat_Class, fieldNew, "text", "50")   # add new field in input feature class attribute table

# Pg2

count = 1                                                       # set counter variable as 1

with arcpy.da.UpdateCursor(feat_Class, fieldList) as upCursor:  # combine WITH with cursor creation to avoid data lock

    for row in upCursor:            # loop to search cursor over feature class and retrieve field values
        strAddress = row[0]
        strCity = row[1]
        strState = row[2]
        strZip = row[3]

        # combine field values into full address string
        strFullAdr = strAddress + ", " + strCity + ", " \
        + strState + strZip
        row[4] = strFullAdr                 # assign full address string into new field
        upCursor.updateRow(row)             # use updateRow function to commit the edit

        print("Update record number: {0}".format(count))        # print confirmation message
        count = count + 1                                       # increment counter variable

print("Update complete")                                        # print completion message
del upCursor                                                    # delete update cursor
