###################################################################################################
# Program: PA20-2 script to fix broken data links
# Author: Abhishek Zeley
# Date: Dec 10, 2021
# Last modified: Dec 10, 2021
####################################################################################################

# ---------- import required modules and set over writing output as True ----------
import arcpy, os, sys
arcpy.env.overwriteOutput = True

# ---------- take user inputs for pathname of project file, new data source and output project file ----------
inAprx = arcpy.GetParameterAsText(0)
newPath = arcpy.GetParameterAsText(1)
outAprx = arcpy.GetParameterAsText(2)

# inAprx = r"C:\Users\nwb31\Desktop\PA3\PA20\Projects\SanAntonioBroken.aprx"
# newPath = r"C:\Users\nwb31\Desktop\PA3\PA20\Data\CityOfSanAntonio.gdb"
# outAprx = "Zeley02"

# ---------- Retrieve project file name ----------
aprxName = arcpy.Describe(inAprx).baseName
message = "The current ArcGIS Project is: {0}.".format(aprxName)
# print(message)
arcpy.AddMessage(message)

# ---------- check if new data source workspace type is geodatabase ----------
if arcpy.Describe(newPath).workspaceType != "LocalDatabase":
    message = "This script only support local database connection."
    sys.exit(message)

# ---------- create ArcGISProject object and list of layers with broken data connection ----------
curAprx = arcpy.mp.ArcGISProject(inAprx)
lstBrklyr = curAprx.listBrokenDataSources()

# ---------- loop through each layer in the broken data connection list ----------
for lyr in lstBrklyr:
    message = "The data link for layer - {0} - is broken. \n" \
              "The original connection path is - {1}. \n " \
              "Save the new connection path as - {2}."\
              .format(lyr.name, lyr.dataSource,
                      newPath + os.sep + os.path.basename(lyr.dataSource))
    # print(message)
    arcpy.AddMessage(message)
    lyr.updateConnectionProperties(os.path.dirname(lyr.dataSource), newPath)    # update new data connection

# ---------- Save the modified project to a new project ----------
newAprx = arcpy.Describe(inAprx).path + os.sep + outAprx + ".aprx"
curAprx.saveACopy(newAprx)
message = "Save the fixed links project as a new project {0}.".format(newAprx)
# print(message)
arcpy.AddMessage(message)

del curAprx, lyr    # delete variables
