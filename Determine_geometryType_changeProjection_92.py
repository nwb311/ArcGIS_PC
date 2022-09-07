###################################################################################################
# Program: Determine geometry type, change projection and use different tools based on geometry type
# Author: Abhishek Zeley
# Date: Nov 5, 2021
# Last modified: Nov 5, 2021
# Description:  Script to determine geometry type, use conditional statements to perform different tool operations and
#               create new feature class based on template feature class

# Variables:
#   outputWS:       store output workspace
#   outTemplate:    store path of feature class used as template
#   outCS:          coordinate system of feature class used as template
#   fcs:            list of feature class in current workspace
#   fc:             store feature class
#   outfc:          store output feature class
#   desc:           description of feature class
#   shapeType:      geometry of feature class
#   prjfc:          store projected feature class
#   outBuf:         store output of buffer tool
#   cleanfcs:       list of feature class to be deleted
#   cleanfc:        store feature class to be deleted

###################################################################################################

import arcpy, os                                                    # import arcpy and os modules

arcpy.env.workspace = arcpy.GetParameterAsText(0)                   # take user input for current workspace
outputWS = arcpy.GetParameterAsText(1)                              # take user input for output workspace
outTemplate = arcpy.GetParameterAsText(2)                           # take user input for template feature class

arcpy.env.overwriteOutput = True                                    # enable overwrite output when re-running the script

outCS = arcpy.Describe(outTemplate).SpatialReference                # obtain spatial reference of template

fcs = arcpy.ListFeatureClasses()                                    # list of all feature classes in current workspace
for fc in fcs:                                                      # for loop to process each feature class
    outfc = outputWS + os.sep + fc + ".shp"                         # output feature class
    desc = arcpy.Describe(fc)                                       # description of feature class
    shapeType = desc.ShapeType                                      # geometry of feature class

    arcpy.AddMessage("Output is {0} as {1}.".format(outfc, shapeType))  # print output feature class and it's geometry

    if shapeType == "Polygon":                                      # conditional statement if geometry is polygon
        arcpy.Project_management(fc, outfc, outCS)   # change feature class projection to that of template feature class
        arcpy.AddMessage("Project {0} to {1}.".format(fc, outfc))  # print change in projection message

    elif shapeType == "Polyline":                                   # conditional statement if geometry is polygon
        prjfc = fc + "_prj"                                   # store intermediate feature class with changed projection
        arcpy.Project_management(fc, prjfc, outCS)   # change feature class projection to that of template feature class
        arcpy.Clip_analysis(prjfc, outTemplate, outfc)              # clip projected feature class per the template fc
        arcpy.AddMessage("Project and clip {0} to {1}.".format(fc, outfc))  # print clip and changed projection message

    elif shapeType == "Point":
        prjfc = fc + "_prj"                                   # store intermediate feature class with changed projection
        arcpy.Project_management(fc, prjfc, outCS)   # change feature class projection to that of template feature class
        arcpy.Clip_analysis(prjfc, outTemplate, outfc)              # clip projected feature class per the template fc
        arcpy.AddMessage("Project and clip {0} to {1}.".format(fc, outfc))  # print clip and changed projection message

        outBuf = outfc[:-4] + "_buf.shp"                            # store buffer tool output
        arcpy.Buffer_analysis(outfc, outBuf, "100 Miles")           # execute buffer tool
        arcpy.AddMessage("Create 100 miles buffer as {0}.".format(outBuf))     # print buffer applied message

cleanupfcs = arcpy.ListFeatureClasses("*_prj")                      # list of intermediate feature classes to be deleted

for cleanfc in cleanupfcs:                             # for loop to process deletion of each intermediate feature class
    arcpy.Delete_management(cleanfc)                   # delete feature class
    arcpy.AddMessage("Delete {0}.".format(cleanfc))    # print deletion message
