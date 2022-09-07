###################################################################################################
# Program: Convert shape file to geodatabase feature class and change shapefile projection per desired template
# Author: Abhishek Zeley
# Date: Nov 5, 2021
# Last modified: Nov 6, 2021
# Description:
#       Take user input for workspace and desired template
#       Convert input shapefile to geodatabase feature class
#       Change projection of shapefile to that of desired template and reflect re-projection information in file name
#
# Variables:
#   outputWS:       user input for output workspace
#   outTemplate:    user input for path of feature class used as template
#   outTemplateName:name string of feature class used as template
#   outCS:          user input for feature class used as template for coordinate system
#   outCSName:      name string of coordinate system template
#   fcs:            list of feature class in current workspace
#   fc:             feature class to be processed from the list
#   fcCSName:       name string for coordinate system of feature class
#   outfc:          store output feature class
#   cpyfc:          feature class to be created in the geodatabase
#   prjfc:          store projected feature class
#   prjfcCSName:    name string for coordinate system of re-projected feature class

###################################################################################################

import arcpy, os                                                  # import arcpy and os modules

arcpy.env.workspace = arcpy.GetParameterAsText(0)                 # user input for current workspace
outWS = arcpy.GetParameterAsText(1)                               # user input for output workspace
outTemplate = arcpy.GetParameterAsText(2)                         # user input for template feature class
outTemplateName = arcpy.Describe(outTemplate).baseName            # name string of template feature class

arcpy.env.overwriteOutput = True                                  # enable overwrite output when re-running the script

outCS = arcpy.Describe(outTemplate).SpatialReference              # coordinate system of template feature class
outCSName = arcpy.Describe(outTemplate).SpatialReference.Name     # name string template feature class coordinate system

fcs = arcpy.ListFeatureClasses()                                  # list of all feature classes in current workspace

for fc in fcs:                                                    # for loop to process each feature class
    fcCSName = arcpy.Describe(fc).SpatialReference.Name           # name string of feature class coordinate system

    if fcCSName == outCSName:                            # check if feature class coordinate system is same as template
        arcpy.AddMessage("{0} and {1} are both in {2}.".format(fc, outTemplateName, outCSName))  # verification message

        cpyfc = outWS + os.sep + fc[:-4]                         # create feature class in geodatabase to be copied into
        arcpy.CopyFeatures_management(fc, cpyfc)                 # copy input shapefile to geodatabase feature class
        arcpy.AddMessage("Copy {0} to {1}.".format(fc, outWS))   # verification message

    else:
        prjfc = outWS + os.sep + fc[:-4] + "_prj"                # create feature class in geodatabase to be copied into
        arcpy.Project_management(fc, prjfc, outCS)               # re-project shapefile per template CS

        prjfcCSName = arcpy.Describe(prjfc).SpatialReference.Name   # name string of re-projected CS
        arcpy.AddMessage("{0} has been projected from {1} to {2}.".format(fc, fcCSName, prjfcCSName))  # verificatn msg
