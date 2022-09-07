###################################################################################################
# Program: script tool in ArcGIS for Buffer and Clip
# Author: Abhishek Zeley
# Date: Nov 4, 2021
# Last modified: Nov 4, 2021
# Description:  write script in IDE
#               use GetParameterAsText in arcpy module (similar to input function in python) to get inputs from user
#               use Buffer tool in analysis toolbox
#               use Clip tool in analysis toolbox
#               use AddMessage function in arcpy to include a message to display at end of analysis
# Variables:
#   inFeatures:     path of file to be written in
#   bufDistance:    buffer distance input from user
#   clipFeatures:   feature used to clip
#   outWorkspace:   workspace to store outputs
#   outName:        name of output file
#   Buffer_Output:  store output of buffer tool
#   Clip_Output:    store output of clip tool
#
# Input parameters: inFeatures, bufDistance, clipFeatures, outWorkspace, outName
# Output: Buffer_Output, Clip_Output

###################################################################################################

import arcpy, os, sys                                           # import arcpy

inFeature = arcpy.GetParameterAsText(0)                         # take input file from user
bufDistance = arcpy.GetParameterAsText(1)                       # take buffer distance input from user
clipFeature = arcpy.GetParameterAsText(2)                       # take clip file from user
outWorkspace = arcpy.GetParameterAsText(3)                      # take workspace path to store output file
outName = arcpy.GetParameterAsText(4)                           # take output file name from user

arcpy.env.overwriteOutput = True                                # enable overwrite output when rerunning the script

Buffer_Output = outWorkspace + os.sep + outName + "buf"         # path to store output of buffer tool
Clip_Output = outWorkspace + os.sep + outName                   # path to store output of clip tool

arcpy.analysis.Buffer(inFeature, Buffer_Output, bufDistance, "Full", "ROUND", "ALL", "")            # use Buffer tool
arcpy.analysis.Clip(Buffer_Output, clipFeature, Clip_Output)    # use Clip tool in analysis toolbox

arcpy.AddMessage("All Done!")                                   # include message after performing analysis
