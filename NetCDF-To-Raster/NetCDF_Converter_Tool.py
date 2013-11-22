#################################
# NASA DEVELOP Program
# Location: Jet Propulsion Laboratory, Pasadena, Ca
# Author: Scott Barron, scottbarron13@gmail.com
# NetCDF Converter: This tool is used to batch convert NetCDF files (which are not viewable with ArcGIS) into raster files (which are).
#################################

import os
import arcpy
from arcpy import env
#The folder_path is the name and location of the folder containing the NetCDF files, and where the rasters will be created.
Input_folder= arcpy.GetParameterAsText(0)
arcpy.env.workspace= Input_folder

#This is the variable to display from the NetCDF file. To assign the default value, leave as NetCDF_Var= "".
Variable= arcpy.GetParameterAsText(1)
                    
#This is the X dimension from the NetCDF file. To assign the default value, leave as NetCDF_X= "".
X_Value= arcpy.GetParameterAsText(2)
    
#This is the Y dimension from the NetCDF file. To assign the default value, leave as NetCDF_Y= "".
Y_Value= arcpy.GetParameterAsText(3)

#This is the name and location where the rasters will be generated.
Output_Location= arcpy.GetParameterAsText(4)

#This for loop will search through the folder designated by folder_path and if a file ends in ".nc", then this script will convert it to a raster.
for NetCDFs in os.listdir(folder_path):
    if NetCDFs[-3:]== ".nc":
        NetCDF_Name= NetCDFs[5:13]
        print NetCDF_Name
        print Output_Location + "/" + NetCDF_Name
        arcpy.MakeNetCDFRasterLayer_md(NetCDFs,Variable,X_Value,Y_Value,NetCDF_Name)
        Raster_Name= "x" + str(NetCDF_Name)
        arcpy.CopyRaster_management(NetCDF_Name,Output_Location + "/" + Raster_Name)

arcpy.AddMessag("The rasters have been successfully generated.")
