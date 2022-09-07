###################################################################################################
# Program: script to classify population as low, medium, high in a newly added field
# Author: Abhishek Zeley
# Date: Nov 14, 2021
# Last modified: Nov 16, 2021
####################################################################################################

import arcpy                                                    # import module

# ------- Take inputs from user ---------
inputFC = arcpy.GetParameterAsText(0)                           # variable to store shapefile
popField = arcpy.GetParameterAsText(1)                          # name of field containing population for 2000
fieldNew = arcpy.GetParameterAsText(2)                          # name of new field to be added

# inputFC = r"C:\Users\nwb31\Desktop\PA3\lab06\Data\MOcnty.shp"  # variable to store shapefile
# popField = "POP2000"                                           # name of field containing population for 2000
# fieldNew = "PopCategory"                                       # name of new field to be added

arcpy.env.workspace = arcpy.Describe(inputFC).path              # specify workspace
feat_Class = arcpy.Describe(inputFC).file                       # variable to store file name


# ------ Validate new field name format, check and delete if it already exist, create new field --------

fieldNew = arcpy.ValidateFieldName(fieldNew)     # function to validate if field name is valid per ArcGIS requirements

# loop to check if new field name already exist in attribute table and if yes, then delete existing field
fields = arcpy.ListFields(feat_Class, fieldNew)                # store list of existing field names

for fld in fields:
    arcpy.DeleteField_management(feat_Class, fieldNew)

# add new field in input feature class attribute table
arcpy.AddField_management(feat_Class, fieldNew, "TEXT", "10")


# -------- Use UpdateCursor to assign value in the newly added field based on population --------

fieldList = [popField, fieldNew, "NAME"]            # variable to store field names to be used by UpdateCursor

with arcpy.da.UpdateCursor(feat_Class, fieldList) as upCursor:  # combine WITH with cursor creation to avoid data lock

    for row in upCursor:                            # loop to search cursor over feature class and retrieve field values
        if row[0] < 10000:                          # check if POP2000 is less than 10000
            row[1] = "LOW"                          # assign LOW in the new field

        elif row[0] > 100000:                       # check if POP2000 is greater than 100000
            row[1] = "HIGH"                         # assign HIGH in the new field

        else:                                       # if 10000 <= POP2000 <= 100000
            row[1] = "MEDIUM"                       # assign MEDIUM in the new field

        upCursor.updateRow(row)                     # use updateRow function to commit the edit

        print("{0} has population of {1} as {2}".format(row[2], row[0], row[1]))    # print desired message


# ----- Use SearchCursor to calculate total number of counties with LOW, MEDIUM and HIGH values in the new field -------

# define counting variables
low = 0
med = 0
high = 0

with arcpy.da.SearchCursor(feat_Class, fieldNew) as srCursor:  # combine WITH with cursor creation to avoid data lock

    for row in srCursor:              # loop to search cursor over feature class and retrieve field values
        if row[0] == "LOW":           # check if new field value is LOW
            low = low + 1             # increment counting variable

        elif row[0] == "MEDIUM":      # check if new field value is MEDIUM
            med = med + 1             # increment counting variable

        elif row[0] == "HIGH":        # check if new field value is HIGH
            high = high + 1           # increment counting variable


# -------- Calculate total number of counties in feat_Class --------
totCnty = arcpy.GetCount_management(feat_Class)     # get count of features in the feature class


# print message to show how many counties have low, medium, high population
print("\nThere are {0} out of {1} counties with LOW population.".format(low, totCnty))
print("There are {0} out of {1} counties with MEDIUM population.".format(med, totCnty))
print("There are {0} out of {1} counties with HIGH population.".format(high, totCnty))

# arcpy.AddMessage("There are {0} out of {1} counties with LOW population.".format(low, totCnty))
# arcpy.AddMessage("There are {0} out of {1} counties with MEDIUM population.".format(med, totCnty))
# arcpy.AddMessage("There are {0} out of {1} counties with HIGH population.".format(high, totCnty))

# delete cursors
del upCursor                            # delete update cursor
del srCursor                            # delete search cursor
