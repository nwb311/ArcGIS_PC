###################################################################################################
# Program: script to use the search cursor to perform analysis based on the field value
# Author: Abhishek Zeley
# Date: Nov 11, 2021
# Last modified: Nov 11, 2021
####################################################################################################

import arcpy            # import module

# define variables to store feature class and list of field names
inputFC = r"C:\Users\nwb31\Desktop\PA3\PA11\Data\MOcnty.shp"
fieldList = ["NAME", "POP2000"]

# assign file path to workspace
arcpy.env.workspace = arcpy.Describe(inputFC).path
feat_Class = arcpy.Describe(inputFC).file

# initiate variables population average, total and count of records
average = 0
totalPopulation = 0
recordCount = 0

with arcpy.da.SearchCursor(feat_Class, fieldList) as srCursor:      # use 'with' with cursor creation to avoid data lock
    for row in srCursor:                                            # iterate through each item until end of record
        print("{0} has population {1})".format(row[0], row[1]))     # print population for each record
        totalPopulation = totalPopulation + row[1]                  # calculate total population
        recordCount = recordCount + 1                               # increment record count variable

# calculate and print average population
average = totalPopulation / recordCount
print("Average population for a county is {0}.".format(average))

del srCursor            # delete search cursor
