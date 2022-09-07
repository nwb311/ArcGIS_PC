###################################################################################################
# Program: script to use insert cursor to add a record into feature class
# Author: Abhishek Zeley
# Date: Nov 13, 2021
# Last modified: Nov 13, 2021
####################################################################################################

import arcpy        # import module

inputFC = r"C:\Users\nwb31\Desktop\PA3\PA12\Data\MOHigherEd.shp"    # variable to store input file
fieldList = ["TYPE", "SHAPE@XY"]                                    # specify list of fields to be accessed by cursor

arcpy.env.workspace = arcpy.Describe(inputFC).path                  # specify workspace
feat_Class = arcpy.Describe(inputFC).file                           # variable to store file name

# initialize the variables for x, y coordinate and one attribute

row_values = [('Pseudo', (400000, 4400000)),
              ('Pseudo', (400000, 4300000))]

isCursor = arcpy.da.InsertCursor(feat_Class, fieldList)     # cursor for input feature class fields listed in fieldList

# loop for each point in the list row_values
for newUniversity in row_values:
    isCursor.insertRow(newUniversity)       # use insert function to add new point in the dataset
    print("Add New University")             # print confirmation message

del isCursor                                # delete cursor
