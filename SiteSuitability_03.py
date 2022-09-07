###################################################################################################
# Program: script to find suitable area within the Study Area which is at a distance from a feature
# Author: Abhishek Zeley
# Date: Nov 6, 2021
# Last modified: Nov 6, 2021
# Description:  use GetParameterAsText in arcpy module to get inputs from user
#               use Buffer tool to create buffer around feature to be avoided
#               use Erase tool to erase buffered area from the Study Area
#               use AddMessage function to display a message at end of analysis
# Variables:
#   studyArea:      study area specified by user
#   fcAvoid:        feature to be avoided
#   bufDistance:    buffer distance input from user
#   outWorkspace:   workspace to store outputs given by user
#   outName:        name of output file given by user
#   Buffer_Output:  store output of buffer tool
#   Erase_Output:    store output of erase tool
#
# Input parameters: studyArea, fcAvoid, bufDistance, outWorkspace, outName

###################################################################################################

import arcpy, os                                                # import arcpy

studyArea = arcpy.GetParameterAsText(0)                         # user input for study area
fcAvoid = arcpy.GetParameterAsText(1)                           # user input for line or point feature to be avoided
bufDistance = arcpy.GetParameterAsText(2)                       # user input for buffer distance
outWorkspace = arcpy.GetParameterAsText(3)                      # user input for output workspace
outName = arcpy.GetParameterAsText(4)                           # user input fpr output file name

arcpy.env.overwriteOutput = True                                # enable overwrite output when rerunning the script

Buffer_Output = outWorkspace + os.sep + fcAvoid + "_buf"        # store output of buffer tool
Erase_Output = outWorkspace + os.sep + outName                  # store output of erase tool

arcpy.analysis.Buffer(fcAvoid, Buffer_Output, bufDistance, "Full", "ROUND", "ALL", "")    # use Buffer tool
arcpy.analysis.Erase(studyArea, Buffer_Output, Erase_Output)    # erase buffer output from study area

arcpy.AddMessage("All Done!")                                   # include message after performing analysis
