import arcpy
#Makes sure Spatial Analyst is turned on.
if arcpy.CheckExtension("Spatial")== "Available":
    arcpy.CheckOutExtension("Spatial")
    from arcpy.sa import *
else:
    arcpy.AddError("You do not have the Spatial Analyst Extension, and therefore cannot use this tool.")
    
#Input folder.
folder= raw_input("Please enter the folder name and path where the data is located: ")
folder_path= r"%s" %folder
arcpy.env.workspace= folder_path

#Masking file.
Mask= raw_input("Please enter the shapefile name that will be used to mask the data: ")
Mask_file= "%s" %Mask

#For all the rasters in the file, perform an extract by mask.
for rasters in arcpy.ListRasters():
    print rasters
    #Out name is the Output File name. EBM stands for "Extract By Mask".
    Out_Name= "EBM_" + rasters
    outExtractByMask = ExtractByMask(rasters, Mask_file)
    outExtractByMask.save(Out_Name)
