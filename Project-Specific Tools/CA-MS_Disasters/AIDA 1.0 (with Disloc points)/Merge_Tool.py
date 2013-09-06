####################
# NASA DEVELOP Program
# LOCATION: Jet Propulsion Laboratory
# TERM: Summer 2013
# TEAM: CA/MS Disasters and Water Resources
# This Infrastructure Batch Merge tool simply takes any number of input polyline files and merges them into one polyline file.
####################

import arcpy
import os
import string
from arcpy import env

#Inputs
File_To_Be_Merged= arcpy.GetParameterAsText(0)
Merge_Output= arcpy.GetParameterAsText(1)

folder_path= File_To_Be_Merged
arcpy.env.workspace= folder_path
file_list= os.listdir(folder_path)
arcpy.env.overwriteOutput= True

#This is a blank list which will contain the shapeiles in the list.
shapefile_name_list=list()
for i in(file_list):
    file_name= i
    file_type= i[-4:]
    if file_type== '.shp':
        shapefile_name_list.append(file_name) #This adds files with ending .shp to our blank list.
#This merges all of the files
arcpy.Merge_management(shapefile_name_list, Merge_Output)
