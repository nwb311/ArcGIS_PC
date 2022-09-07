###################################################################################################
# Program: PA20-1 script to find broken data links
# Author: Abhishek Zeley
# Date: Dec 10, 2021
# Last modified: Dec 10, 2021
####################################################################################################

# ---------- import required modules and set over writing output as True ----------
import arcpy, os
arcpy.env.overwriteOutput = True

# --------- Assign the pathname of folder with possible project or layer file with broken data links ----------
inFolder = arcpy.GetParameterAsText(0)
# inFolder = r"C:\Users\nwb31\Desktop\PA3\PA20"

# -------- loop to search files in the entire folder and its subfolders ------------
for root, dirs, files in os.walk(inFolder):     # root = folder path, dirs = folder name, files = file name
    for name in files:                                              # loop through each file name
        fileName = os.path.join(root, name)                         # for each file, join the file name with path
        if ".aprx" in fileName:                                     # check if file is a project file
            curAprx = arcpy.mp.ArcGISProject(fileName)              # create ArcGISProject object
            message = "The ArcGIS Project is {0}.".format(fileName)  # print path and file name
            arcpy.AddMessage(message)
            # print(message)

            lstBrklyr = curAprx.listBrokenDataSources()            # create a list of layers with broken data connection
            if lstBrklyr == []:                                    # check if broken layer list is empty
                message = "There is no broken link in the " + \
                          "current ArcGIS Project.\n"
                arcpy.AddMessage(message)                          # print confirmation message
                # print(message)  # print confirmation message
            else:
                for lyr in lstBrklyr:                              # if broken layers are present in the list
                    message = "Broken data Links: {0}.".format(lyr.name)
                    arcpy.AddMessage(message)                                 # print name of the broken layer
                    # print(message)  # print name of the broken layer

        if ".lyrx" in fileName:                                    # check if file is a layer
            curLF = arcpy.mp.LayerFile(fileName)                   # create layer file object
            message = "The Layer File is {0}.".format(fileName)
            # print(message)  # print layer name
            arcpy.AddMessage(message)                              # print layer name

            lstBrklyr = curLF.listBrokenDataSources()              # create a list of layers with broken data connection
            if lstBrklyr == []:                                    # check if broken layer list is empty
                message = "There is no broken link in the " + \
                          "current Layer File.\n"
                # print(message)  # print confirmation message
                arcpy.AddMessage(message)                                     # print confirmation message
            else:
                for lyr in lstBrklyr:                              # loop through each layer in the list
                    message = "Broken data links: (0].".format(lyr.name)
                    arcpy.AddMessage(message)                                 # print confirmation message
                    # print(message)  # print confirmation message
message = "\n----------------------All Done---------------------\n"
arcpy.AddMessage(message)                                                     # print confirmation message
# print(message)                                                     # print confirmation message

del curAprx, curLF, lyr                                            # delete variables
