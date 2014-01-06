#################################
#NASA DEVELOP Program
# Location: Jet Propulsion Laboratory, Pasadena, Ca
# Author: Scott Barron, scottbarron13@gmail.com
# NetCDF Converter: This tool is used to batch convert NetCDF files (which are not viewable with ArcGIS) into raster files (which are).
#################################

import os
import arcpy
from arcpy import env
#The folder_path is the name and location of the folder containing the NetCDF files, and where the rasters will be created.
folder= raw_input("Please input the name and location of the folder containing the NetCDFs: ")
folder_path= r"%s" %(folder)
arcpy.env.workspace= folder_path

#This is the variable to display from the NetCDF file. To assign the default value, leave as NetCDF_Var= "".
Variable= raw_input("If you would like to use the default value for 'Variable', type 'Yes'. If not, type 'No'" )
Var= "%s" %Variable
if Var == "Yes":
    NetCDF_Var= ""
elif Var == "No":
    Var2= raw_input("Please enter the 'Variable' value: ")
    NetCDF_Var= "%s" %Var2
else:
    print "You entered an invalid command. Please restart the code and enter either Yes or No when prompted."
                    
#This is the X dimension from the NetCDF file. To assign the default value, leave as NetCDF_X= "".
X_Value= raw_input("If you would like to use the default value for 'X dimension', type 'Yes'. If not, type 'No'")
Value= "%s" %X_Value
if Value == "Yes":
    NetCDF_X= ""
elif Value == "No":
    X_Value2= raw_input("Please enter the 'X dimension' value: ")
    NetCDF_X= "%s" %X_Value2
else:
    print "You entered an invalid command. Please restart the code and enter either Yes or No when prompted."
    
#This is the Y dimension from the NetCDF file. To assign the default value, leave as NetCDF_Y= "".
Y_Value= raw_input("If you would like to use the default value for 'Y dimension', type 'Yes'. If not, type 'No'")
Value= "%s" %Y_Value
if Value == "Yes":
    NetCDF_Y= ""
elif Value == "No":
    Y_Value2= raw_input("Please enter the 'Y dimension' value: ")
    NetCDF_Y= "%s" %Y_Value2
else:
    print "You entered an invalid command. Please restart the code and enter either Yes or No when prompted."

#This is the name and location where the rasters will be generated.
Output_Location= raw_input('Where would you like the generated rasters to be placed?' )
Output= r"%s" %Output_Location

#This for loop will search through the folder designated by folder_path and if a file ends in ".nc", then this script will convert it to a raster.
for NetCDFs in os.listdir(folder_path):
    if NetCDFs[-3:]== ".nc":
        NetCDF_Name= NetCDFs[5:13]
        print NetCDF_Name
        print Output + "/" + NetCDF_Name
        arcpy.MakeNetCDFRasterLayer_md(NetCDFs,NetCDF_Var,NetCDF_X,NetCDF_Y,NetCDF_Name)
        Raster_Name= "x" + str(NetCDF_Name)
        arcpy.CopyRaster_management(NetCDF_Name,Output + "/" + Raster_Name)

print "The rasters have been successfully generated."
