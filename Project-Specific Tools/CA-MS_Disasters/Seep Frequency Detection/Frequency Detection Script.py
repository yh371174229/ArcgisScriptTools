####################
# NASA DEVELOP Program
# LOCATION: Jet Propulsion Laboratory
# TERM: Summer 2013
# TEAM: CA/MS Disasters and Water Resources
# This Frequency Detection tool will take any number of input seep detection files and sum their values to locate areas of consistent seepage
####################

import arcpy
import os
import math
import string
import arcgisscripting
from arcpy import env
if arcpy.CheckExtension("Spatial")== "Available":
    arcpy.CheckOutExtension("Spatial")
    from arcpy.sa import *
else:
    arcpy.AddMessage("You do not have the Spatial Analyst Extension, and therefore cannot use this tool.")
arcpy.env.overwriteOutput= True

#User Inputs
#The folder_path variable is the folder that contains all of the raster data for the tool.
folder_path= arcpy.GetParameterAsText(0)
Output_Raster= "DEL_Output"
#This is the output location and name of the seep frequency raster.
Reclass_Output= arcpy.GetParameterAsText(1)
Kmz_Name= arcpy.GetParameterAsText(2)
Kmz_Var= folder_path + "/" + str(Kmz_Name) + ".kmz"


#If the Reclass_Output name is more than 8 characters, the tool won't run and will return a confusing error message that does not explain the problem. This takes care of that.
(path,file_name)=os.path.split(Reclass_Output)
if len(file_name)>=9:
    arcpy.AddError(" ")
    arcpy.AddError(" ")
    arcpy.AddError("The 'Output' name you have entered is too long. Please rerun the tool with a name 8 characters or less.")

#Workspace syntax
arcpy.env.workspace= folder_path
gp= arcgisscripting.create(10.1)
gp.workspace= folder_path

#This is an iteration counter used by the if statements below.
x=0

#This list is used to store the most recent output of the raster addition function and recall it to be used in the next iteration.
main_list= list()

#Creates a list of GRIDs in the workspace.
Rasters = gp.ListRasters("", "GRID")

#For loop searching through the total list of rasters.
for raster in Rasters:
    if len(raster)==13:
    #Creates a temporary list to store the most recent selected raster file from the folder. 
        temp_list= list()
        temp_list.append(raster)
        #If it is the first iteration, the script will skip the raster addition step because there is nothing to add. Instead it takes the first raster from the folder and places it in the main_list to be called upon next iteration.
        if x== 0:                      
            main_list.append(raster)
        #If it is after the first iteration then the raster addition function will be used.
        if x >= 1:
            #This labels the Output_Raster with the number of the iteration. 
            Output_Raster= "Out_Ras" + str(x)
            #This is the raster addition function, it takes the last value in both the main_list and temp_list and sums them.
            outPlus= Raster(main_list[-1])+Raster(temp_list[-1])
            outPlus.save(Output_Raster)
            #This takes the sum above and appends it to the main_list to be used in the raster addition function in the next iteration.
            main_list.append(Output_Raster)
        #This adds one to the iteration counter.
        x= x+1

#Reclassify the last Output_Raster, which is the sum of all the rasters, to make sure the output is in a unique values.
Reclass= Reclassify(Output_Raster, "Value", RemapValue([[-1,0,0],[0,1,1],[1,2,2],[2,3,3],[3,4,4],[4,5,5],[5,6,6],[6,7,7],[7,8,8],[8,9,9],[9,10,10],[10,11,11],[11,12,12],[12,13,13],[13,14,14],[14,15,15],[15,16,16],[16,17,17],[17,18,18],[18,19,19],[19,20,20],[20,21,21],[21,22,22],[22,23,23],[23,24,24],[24,25,25],[25,26,26],[26,27,27],[27,28,28],[28,29,29],[29,30,30],[30,31,31],[31,32,32],[32,33,33],[33,34,34],[34,35,35],[35,36,36],[36,37,37],[37,38,38],[38,39,39],[39,40,40],[40,41,41]]))
Reclass.save(Reclass_Output)

#Reclassify again, this time valuing -1 to 0 as No Data.
Reclass2= Reclassify(Reclass_Output, "Value", RemapValue([[-1,0,"NoData"],[0,1,1],[1,2,2],[2,3,3],[3,4,4],[4,5,5],[5,6,6],[6,7,7],[7,8,8],[8,9,9],[9,10,10],[10,11,11],[11,12,12],[12,13,13],[13,14,14],[14,15,15],[15,16,16],[16,17,17],[17,18,18],[18,19,19],[19,20,20],[20,21,21],[21,22,22],[22,23,23],[23,24,24],[24,25,25],[25,26,26],[26,27,27],[27,28,28],[28,29,29],[29,30,30],[30,31,31],[31,32,32],[32,33,33],[33,34,34],[34,35,35],[35,36,36],[36,37,37],[37,38,38],[38,39,39],[39,40,40],[40,41,41]]))
Reclass2.save("DEL_Reclass")

#Convert raster to polygon in order to make kmz.
Polygon= "Freq.shp"
arcpy.RasterToPolygon_conversion("DEL_Reclass", Polygon, "NO_SIMPLIFY", "VALUE")
    
#Make Feature Layer
Del= Kmz_Name
arcpy.MakeFeatureLayer_management(Polygon, Del)

#Convert layer to kmz
arcpy.LayerToKML_conversion(Del, Kmz_Var)
