####################
# NASA DEVELOP Program
# LOCATION: Jet Propulsion Laboratory
# TERM: Summer 2013
# TEAM: CA/MS Disasters and Water Resources
# This Change Detection tool takes two different Seep Detection outputs (rasters) and compares the locations of the seeps to highlight differences.
####################

import os
import string
import arcpy
from arcpy import env
if arcpy.CheckExtension("Spatial")== "Available":
    arcpy.CheckOutExtension("Spatial")
    from arcpy.sa import *
else:
    arcpy.AddError("You do not have the Spatial Analyst Extension, and therefore cannot use this tool.")
    print "You do not have the Spatial Analyst Extension, and therefore cannot use this tool."
arcpy.env.overwriteOutput= True
#os.path.basename(Seep_1)

#Inputs
#The Work Folder is the location of all the seep detection rasters created by the seep detection tool.
Work_folder= arcpy.GetParameterAsText(0)
#Seep_1 is the first flight date the tool will look at.
Seep_1= arcpy.GetParameterAsText(1)
#Seep_2 is the second flight date the tool will look at.
Seep_2= arcpy.GetParameterAsText(2)
#Raster Output
raster= arcpy.GetParameterAsText(3)
File_Name= str(Seep_1[-12:-7]) + "_" + str(Seep_1[-6:-1]) + "_" + str(Seep_2[-12:-7]) + "_" + str(Seep_2[-6:-1])

#Workspace
env.workspace= Work_folder

#Multiply by 2
Multiply= Raster(Seep_2) * 2
Multiply.save("Seep_2x")

#A(First flight) + 2B (Second flight multiplied by 2)
Addition= Plus(Seep_1, "Seep_2x")
Addition.save(raster)

#Conditional statemetns to break up the different types of seep changes.
outCon0 = Con(raster, raster, "", """"VALUE"= 0""")
outCon0.save("No_Seep")
outCon1 = Con(raster, raster, "", """"VALUE"= 1""")
outCon1.save("Decrease")
outCon2 = Con(raster, raster, "", """"VALUE"= 2""")
outCon2.save("Increase")
outCon3 = Con(raster, raster, "", """"VALUE"= 3""")
outCon3.save("Consist")

#Raster to Polygon
arcpy.RasterToPolygon_conversion("No_Seep", "No_Seep.shp", "NO_SIMPLIFY", "VALUE")
arcpy.RasterToPolygon_conversion("Decrease", "Decreasing.shp", "NO_SIMPLIFY", "VALUE")
arcpy.RasterToPolygon_conversion("Increase", "Increasing.shp", "NO_SIMPLIFY", "VALUE")
arcpy.RasterToPolygon_conversion("Consist", "Consistent.shp", "NO_SIMPLIFY", "VALUE")

#Make Feature Layer
arcpy.MakeFeatureLayer_management("No_Seep.shp", "No_Seep.lyr")
arcpy.MakeFeatureLayer_management("Decreasing.shp", "Decreasing.lyr")
arcpy.MakeFeatureLayer_management("Increasing.shp", "Increasing.lyr")
arcpy.MakeFeatureLayer_management("Consistent.shp", "Consistent.lyr")
             

#Save To Layer File
arcpy.SaveToLayerFile_management("No_Seep.lyr", Work_folder + "/" + File_Name+ "No_Seep" + ".lyr", "ABSOLUTE", "CURRENT")
arcpy.SaveToLayerFile_management("Decreasing.lyr", Work_folder + "/" + File_Name+ "Decreasing" + ".lyr", "ABSOLUTE", "CURRENT")
arcpy.SaveToLayerFile_management("Increasing.lyr", Work_folder + "/" + File_Name+ "Increasing" + ".lyr", "ABSOLUTE", "CURRENT")
arcpy.SaveToLayerFile_management("Consistent.lyr", Work_folder + "/" + File_Name+ "Consistent" + ".lyr", "ABSOLUTE", "CURRENT")

# Process: Layer To KML
arcpy.LayerToKML_conversion(Work_folder + "/" + File_Name+ "No_Seep" + ".lyr", Work_folder + "/" + File_Name+ "No_Seep" + ".kmz", "1", "false", "DEFAULT", "1024", "96", "CLAMPED_TO_GROUND")
arcpy.LayerToKML_conversion(Work_folder + "/" + File_Name+ "Decreasing" + ".lyr", Work_folder + "/" + File_Name+ "Decreasing" + ".kmz", "1", "false", "DEFAULT", "1024", "96", "CLAMPED_TO_GROUND")
arcpy.LayerToKML_conversion(Work_folder + "/" + File_Name+ "Increasing" + ".lyr", Work_folder + "/" + File_Name+ "Increasing" + ".kmz", "1", "false", "DEFAULT", "1024", "96", "CLAMPED_TO_GROUND")
arcpy.LayerToKML_conversion(Work_folder + "/" + File_Name+ "Consistent" + ".lyr", Work_folder + "/" + File_Name+ "Consistent" + ".kmz", "1", "false", "DEFAULT", "1024", "96", "CLAMPED_TO_GROUND")

