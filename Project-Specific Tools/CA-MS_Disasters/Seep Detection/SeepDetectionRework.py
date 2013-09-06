####################
# NASA DEVELOP Program
# LOCATION: Jet Propulsion Laboratory
# TERM: Summer 2013
# TEAM: CA/MS Disasters and Water Resources
# This Seep Detection tool takes UAVSAR Polarimetric Radar images in bands VV and HH, and uses them to locate areas of levee seepage. 
####################

import arcpy
import os
import string
from arcpy import env
if arcpy.CheckExtension("Spatial")== "Available":
    arcpy.CheckOutExtension("Spatial")
    from arcpy.sa import *
else:
    arcpy.AddError("You do not have the Spatial Analyst Extension, and therefore cannot use this tool.")
arcpy.env.overwriteOutput= True

#Inputs
#Raster_folder is the folder name and location where all the rasters are located.
Raster_folder= arcpy.GetParameterAsText(0)

#Frequency_folder is the folder that will be used to house the reclassified rasters that will be used as inputs in the frequency detection tool. It should be different from the Raster_folder.
Frequency_folder= arcpy.GetParameterAsText(1)

#Buffer_Shapefile is the buffer that extendeds out from the levees.
Buffer_Shapefile= arcpy.GetParameterAsText(2)

#Symbology_Layer is the layer file that contains the symbology information for the final outputs.
Symbology_Layer=  arcpy.GetParameterAsText(3)

#Mask.
Mask= arcpy.GetParameterAsText(4)

#Region group value.
z= arcpy.GetParameterAsText (5) #"Count >= 10"

#Lists
#The HH_raster_list is the list with all the HH rasters.
HH_raster_list= list()
#The VV_raster_list is the list with all the VV rasters.
VV_raster_list= list()
#The date list will house the different flight dates used in this tool and allow for index labeling.
date_list= list()
#The flight list will house the different flight paths used in this tool and allow for index labeling.
flight_list= list()
#The time list will house the different flight times used in this tool and allow for index labeling.
time_list= list()

#Iteration Counter
x=0

#First workspace. This is where most of the processing will occur.
env.workspace = Raster_folder

###############################################
#Below is a bunch of nested if statements in a for loop. Overall, these if statements look at every raster in the Raster_folder
#and make a number of decisions about them. First, they check if the raster name has atleast 40 characters, as the PolSAR files this
#tool is designed to look at are quite long. Next, it checks if the flight date, path, and time have been added to the appropriate
#lists above. If they have, then the if statements will attach an indexed location to the working file name. If not, then the tool
#first adds the information to the appropriate lists and then indexes the location. In order to make this tool work on a very large
#(50 or less) number of files, we then included another if statement that will turn the indexing values into two digits. A more
#detailed description of what each if statement does can be found below.
###############################################

#Raster for loop. This searchs for all the rasters in the Raster_folder
for raster in arcpy.ListRasters():
    #If the length of the rasters are 40 characters or longer, then we can assume the raster is one of the original flight rasters.
    if len(raster)>=40:
        #This looks to see if the flight is HH polarization.
        if raster[34:36]== "HH":
            final_index_list= list()
            #If the flight date is in the date_list, then it will add the indexed number of the flight date to the file name.
            if raster[23:29] in date_list:
                #If the flight path is in the flight_list, then it will add the indexed number of the flight path to the file name.
                if raster[7:12] in flight_list:
                    #If the flight time is in the time_list then it will add the indexed number of the flight time to the file name.
                    if raster[20:22] in time_list:
                        i= date_list.index(raster[23:29])
                        a= flight_list.index(raster[7:12])
                        t= time_list.index(raster[20:22])
                        #If the length of the flight date index number is equal to 1, then this statement will add a 0 to the front of it. This is used to make all index values two digits, so that we can have lists longer than 10.
                        if len(str(i))==1:
                            extend=str(i)
                            extended_name= extend.zfill(2)
                            final_index_list.append(extended_name)
                        #If the length of the flight date index number is greater than 1, then we don't add a 0 to the front of it.
                        else:
                            extend= str(i)
                            final_index_list.append(extend)
                        #If the length of the flight path index number is equal to 1, then this statement will add a 0 to the front of it. This is used to make all index values two digits, so that we can have lists longer than 10.
                        if len(str(a))==1:
                            extend= str(a)
                            extended_name= extend.zfill(2)
                            final_index_list.append(extended_name)
                        #If the length of the flight path index number is greater than 1, then we don't add a 0 to the front of it.
                        else:
                            extend= str(a)
                            final_index_list.append(extend)
                        #If the length of the flight time index number is equal to 1, then this statement will add a 0 to the front of it. This is used to make all index values two digits, so that we can have lists longer than 10.
                        if len(str(t))==1:
                            extend= str(t)
                            extended_name= extend.zfill(2)
                            final_index_list.append(extended_name)
                        #If the length of the flight time index number is greater than 1, then we don't add a 0 to the front of it.
                        else:
                            extend= str(t)
                            final_index_list.append(extend)
                        NewName = str(final_index_list[0]) + str(final_index_list[1]) + str(final_index_list[2]) + raster[34:36]
                        arcpy.CopyRaster_management(raster, NewName)
                        HH_raster_list.append(NewName)
                    #If the flight time is not in the time_list, then it will add it to that list and then add the indexed number of the flight time to the file name.  
                    else:
                        i= date_list.index(raster[23:29])
                        a= flight_list.index(raster[7:12])
                        time_list.append(raster[20:22])
                        t= time_list.index(raster[20:22])
                        #If the length of the flight date index number is equal to 1, then this statement will add a 0 to the front of it. This is used to make all index values two digits, so that we can have lists longer than 10.
                        if len(str(i))==1:
                            extend=str(i)
                            extended_name= extend.zfill(2)
                            final_index_list.append(extended_name)
                        #If the length of the flight date index number is greater than 1, then we don't add a 0 to the front of it.
                        else:
                            extend= str(i)
                            final_index_list.append(extend)
                        #If the length of the flight path index number is equal to 1, then this statement will add a 0 to the front of it. This is used to make all index values two digits, so that we can have lists longer than 10.
                        if len(str(a))==1:
                            extend= str(a)
                            extended_name= extend.zfill(2)
                            final_index_list.append(extended_name)
                        #If the length of the flight path index number is greater than 1, then we don't add a 0 to the front of it.
                        else:
                            extend= str(a)
                            final_index_list.append(extend)
                        #If the length of the flight time index number is equal to 1, then this statement will add a 0 to the front of it. This is used to make all index values two digits, so that we can have lists longer than 10.
                        if len(str(t))==1:
                            extend= str(t)
                            extended_name= extend.zfill(2)
                            final_index_list.append(extended_name)
                        #If the length of the flight time index number is greater than 1, then we don't add a 0 to the front of it.
                        else:
                            extend= str(t)
                            final_index_list.append(extend)
                        
                        NewName = str(final_index_list[0]) + str(final_index_list[1]) + str(final_index_list[2]) + raster[34:36]
                        arcpy.CopyRaster_management(raster, NewName)
                        HH_raster_list.append(NewName)
                #If the flight path is not in the flight_list, then it will add it to that list and then add the indexed number of the flight path to the file name.
                else:
                    #If the flight time is in the time_list then it will add the indexed number of the flight time to the file name.
                    if raster[20:22] in time_list:
                        i= date_list.index(raster[23:29])
                        flight_list.append(raster[7:12])
                        a=flight_list.index(raster[7:12])
                        t= time_list.index(raster[20:22])
                        #If the length of the flight date index number is equal to 1, then this statement will add a 0 to the front of it. This is used to make all index values two digits, so that we can have lists longer than 10.
                        if len(str(i))==1:
                            extend=str(i)
                            extended_name= extend.zfill(2)
                            final_index_list.append(extended_name)
                        #If the length of the flight date index number is greater than 1, then we don't add a 0 to the front of it.
                        else:
                            extend= str(i)
                            final_index_list.append(extend)
                        #If the length of the flight path index number is equal to 1, then this statement will add a 0 to the front of it. This is used to make all index values two digits, so that we can have lists longer than 10.
                        if len(str(a))==1:
                            extend= str(a)
                            extended_name= extend.zfill(2)
                            final_index_list.append(extended_name)
                        #If the length of the flight path index number is greater than 1, then we don't add a 0 to the front of it.
                        else:
                            extend= str(a)
                            final_index_list.append(extend)
                        #If the length of the flight time index number is equal to 1, then this statement will add a 0 to the front of it. This is used to make all index values two digits, so that we can have lists longer than 10.
                        if len(str(t))==1:
                            extend= str(t)
                            extended_name= extend.zfill(2)
                            final_index_list.append(extended_name)
                        #If the length of the flight time index number is greater than 1, then we don't add a 0 to the front of it.
                        else:
                            extend= str(t)
                            final_index_list.append(extend)
                        
                        NewName = str(final_index_list[0]) + str(final_index_list[1]) + str(final_index_list[2]) + raster[34:36]
                        arcpy.CopyRaster_management(raster, NewName)
                        HH_raster_list.append(NewName)
                    #If the flight time is not in the time_list, then it will add it to that list and then add the indexed number of the flight time to the file name.
                    else:
                        i= date_list.index(raster[23:29])
                        flight_list.append(raster[7:12])
                        a=flight_list.index(raster[7:12])
                        time_list.append(raster[20:22])
                        t= time_list.index(raster[20:22])
                        #If the length of the flight date index number is equal to 1, then this statement will add a 0 to the front of it. This is used to make all index values two digits, so that we can have lists longer than 10.
                        if len(str(i))==1:
                            extend=str(i)
                            extended_name= extend.zfill(2)
                            final_index_list.append(extended_name)
                        #If the length of the flight date index number is greater than 1, then we don't add a 0 to the front of it.
                        else:
                            extend= str(i)
                            final_index_list.append(extend)
                        #If the length of the flight path index number is equal to 1, then this statement will add a 0 to the front of it. This is used to make all index values two digits, so that we can have lists longer than 10.
                        if len(str(a))==1:
                            extend= str(a)
                            extended_name= extend.zfill(2)
                            final_index_list.append(extended_name)
                        #If the length of the flight path index number is greater than 1, then we don't add a 0 to the front of it.
                        else:
                            extend= str(a)
                            final_index_list.append(extend)
                        #If the length of the flight time index number is equal to 1, then this statement will add a 0 to the front of it. This is used to make all index values two digits, so that we can have lists longer than 10.
                        if len(str(t))==1:
                            extend= str(t)
                            extended_name= extend.zfill(2)
                            final_index_list.append(extended_name)
                        #If the length of the flight time index number is greater than 1, then we don't add a 0 to the front of it.
                        else:
                            extend= str(t)
                            final_index_list.append(extend)
            
                        NewName = str(final_index_list[0]) + str(final_index_list[1]) + str(final_index_list[2]) + raster[34:36]
                        arcpy.CopyRaster_management(raster, NewName)
                        HH_raster_list.append(NewName)

            #If the flight date is not in the date_list, then it will add it to the list and then add the indexed number of the flight date to the file name.
            else:
                if raster[7:12] in flight_list:
                    #If the flight time is in the time_list then it will add the indexed number of the flight time to the file name.
                    if raster[20:22] in time_list:
                        date_list.append(raster[23:29])
                        i= date_list.index(raster[23:29])
                        a= flight_list.index(raster[7:12])
                        t= time_list.index(raster[20:22])
                        #If the length of the flight date index number is equal to 1, then this statement will add a 0 to the front of it. This is used to make all index values two digits, so that we can have lists longer than 10.
                        if len(str(i))==1:
                            extend=str(i)
                            extended_name= extend.zfill(2)
                            final_index_list.append(extended_name)
                        #If the length of the flight date index number is greater than 1, then we don't add a 0 to the front of it.
                        else:
                            extend= str(i)
                            final_index_list.append(extend)
                        #If the length of the flight path index number is equal to 1, then this statement will add a 0 to the front of it. This is used to make all index values two digits, so that we can have lists longer than 10.
                        if len(str(a))==1:
                            extend= str(a)
                            extended_name= extend.zfill(2)
                            final_index_list.append(extended_name)
                        #If the length of the flight path index number is greater than 1, then we don't add a 0 to the front of it.
                        else:
                            extend= str(a)
                            final_index_list.append(extend)
                        #If the length of the flight time index number is equal to 1, then this statement will add a 0 to the front of it. This is used to make all index values two digits, so that we can have lists longer than 10.
                        if len(str(t))==1:
                            extend= str(t)
                            extended_name= extend.zfill(2)
                            final_index_list.append(extended_name)
                        #If the length of the flight time index number is greater than 1, then we don't add a 0 to the front of it.
                        else:
                            extend= str(t)
                            final_index_list.append(extend)
                        
                        NewName = str(final_index_list[0]) + str(final_index_list[1]) + str(final_index_list[2]) + raster[34:36]
                        arcpy.CopyRaster_management(raster, NewName)
                        HH_raster_list.append(NewName)
                    #If the flight time is not in the time_list, then it will add it to that list and then add the indexed number of the flight time to the file name.
                    else:
                        date_list.append(raster[23:29])
                        i= date_list.index(raster[23:29])
                        a= flight_list.index(raster[7:12])
                        time_list.append(raster[20:22])
                        t= time_list.index(raster[20:22])
                        #If the length of the flight date index number is equal to 1, then this statement will add a 0 to the front of it. This is used to make all index values two digits, so that we can have lists longer than 10.
                        if len(str(i))==1:
                            extend=str(i)
                            extended_name= extend.zfill(2)
                            final_index_list.append(extended_name)
                        #If the length of the flight date index number is greater than 1, then we don't add a 0 to the front of it.
                        else:
                            extend= str(i)
                            final_index_list.append(extend)
                        #If the length of the flight path index number is equal to 1, then this statement will add a 0 to the front of it. This is used to make all index values two digits, so that we can have lists longer than 10.
                        if len(str(a))==1:
                            extend= str(a)
                            extended_name= extend.zfill(2)
                            final_index_list.append(extended_name)
                        #If the length of the flight path index number is greater than 1, then we don't add a 0 to the front of it.
                        else:
                            extend= str(a)
                            final_index_list.append(extend)
                        #If the length of the flight time index number is equal to 1, then this statement will add a 0 to the front of it. This is used to make all index values two digits, so that we can have lists longer than 10.
                        if len(str(t))==1:
                            extend= str(t)
                            extended_name= extend.zfill(2)
                            final_index_list.append(extended_name)
                        #If the length of the flight time index number is greater than 1, then we don't add a 0 to the front of it.
                        else:
                            extend= str(t)
                            final_index_list.append(extend)
                        
                        NewName = str(final_index_list[0]) + str(final_index_list[1]) + str(final_index_list[2]) + raster[34:36]
                        arcpy.CopyRaster_management(raster, NewName)
                        HH_raster_list.append(NewName)
                #If the flight path is not in the flight_list, then it will add it to that list and then add the indexed number of the flight path to the file name.
                else:
                    #If the flight time is in the time_list then it will add the indexed number of the flight time to the file name.
                    if raster[20:22] in time_list:                         
                        date_list.append(raster[23:29])
                        i= date_list.index(raster[23:29])
                        flight_list.append(raster[7:12])
                        a=flight_list.index(raster[7:12])
                        t= time_list.index(raster[20:22])
                        #If the length of the flight date index number is equal to 1, then this statement will add a 0 to the front of it. This is used to make all index values two digits, so that we can have lists longer than 10.
                        if len(str(i))==1:
                            extend=str(i)
                            extended_name= extend.zfill(2)
                            final_index_list.append(extended_name)
                        #If the length of the flight date index number is greater than 1, then we don't add a 0 to the front of it.
                        else:
                            extend= str(i)
                            final_index_list.append(extend)
                        #If the length of the flight path index number is equal to 1, then this statement will add a 0 to the front of it. This is used to make all index values two digits, so that we can have lists longer than 10.
                        if len(str(a))==1:
                            extend= str(a)
                            extended_name= extend.zfill(2)
                            final_index_list.append(extended_name)
                        #If the length of the flight path index number is greater than 1, then we don't add a 0 to the front of it.
                        else:
                            extend= str(a)
                            final_index_list.append(extend)
                        #If the length of the flight time index number is equal to 1, then this statement will add a 0 to the front of it. This is used to make all index values two digits, so that we can have lists longer than 10.
                        if len(str(t))==1:
                            extend= str(t)
                            extended_name= extend.zfill(2)
                            final_index_list.append(extended_name)
                        #If the length of the flight time index number is greater than 1, then we don't add a 0 to the front of it.
                        else:
                            extend= str(t)
                            final_index_list.append(extend)

                        NewName = str(final_index_list[0]) + str(final_index_list[1]) + str(final_index_list[2]) + raster[34:36]
                        arcpy.CopyRaster_management(raster, NewName)
                        HH_raster_list.append(NewName)
                    #If the flight time is not in the time_list, then it will add it to that list and then add the indexed number of the flight time to the file name.
                    else:
                        date_list.append(raster[23:29])
                        i= date_list.index(raster[23:29])
                        flight_list.append(raster[7:12])
                        a=flight_list.index(raster[7:12])
                        time_list.append(raster[20:22])
                        t= time_list.index(raster[20:22])
                        #If the length of the flight date index number is equal to 1, then this statement will add a 0 to the front of it. This is used to make all index values two digits, so that we can have lists longer than 10.
                        if len(str(i))==1:
                            extend=str(i)
                            extended_name= extend.zfill(2)
                            final_index_list.append(extended_name)
                        #If the length of the flight date index number is greater than 1, then we don't add a 0 to the front of it.
                        else:
                            extend= str(i)
                            final_index_list.append(extend)
                        #If the length of the flight path index number is equal to 1, then this statement will add a 0 to the front of it. This is used to make all index values two digits, so that we can have lists longer than 10.
                        if len(str(a))==1:
                            extend= str(a)
                            extended_name= extend.zfill(2)
                            final_index_list.append(extended_name)
                        #If the length of the flight path index number is greater than 1, then we don't add a 0 to the front of it.
                        else:
                            extend= str(a)
                            final_index_list.append(extend)
                        #If the length of the flight time index number is equal to 1, then this statement will add a 0 to the front of it. This is used to make all index values two digits, so that we can have lists longer than 10.
                        if len(str(t))==1:
                            extend= str(t)
                            extended_name= extend.zfill(2)
                            final_index_list.append(extended_name)
                        #If the length of the flight time index number is greater than 1, then we don't add a 0 to the front of it.
                        else:
                            extend= str(t)
                            final_index_list.append(extend)

                        NewName = str(final_index_list[0]) + str(final_index_list[1]) + str(final_index_list[2]) + raster[34:36]
                        arcpy.CopyRaster_management(raster, NewName)
                        HH_raster_list.append(NewName)

        #This looks to see if the raster is VV polarization.
        elif raster[34:36]== "VV":
            final_index_list= list()
            #If the flight date is in the date_list, then it will add the indexed number of the flight date to the file name.
            if raster[23:29] in date_list:
                #If the flight time is in the time_list then it will add the indexed number of the flight time to the file name.
                if raster[7:12] in flight_list:
                    #If the flight time is in the time_list then it will add the indexed number of the flight time to the file name.
                    if raster[20:22] in time_list:
                        a= flight_list.index(raster[7:12])
                        i= date_list.index(raster[23:29])
                        t= time_list.index(raster[20:22])
                        #If the length of the flight date index number is equal to 1, then this statement will add a 0 to the front of it. This is used to make all index values two digits, so that we can have lists longer than 10.
                        if len(str(i))==1:
                            extend=str(i)
                            extended_name= extend.zfill(2)
                            final_index_list.append(extended_name)
                        #If the length of the flight date index number is greater than 1, then we don't add a 0 to the front of it.
                        else:
                            extend= str(i)
                            final_index_list.append(extend)
                        #If the length of the flight path index number is equal to 1, then this statement will add a 0 to the front of it. This is used to make all index values two digits, so that we can have lists longer than 10.
                        if len(str(a))==1:
                            extend= str(a)
                            extended_name= extend.zfill(2)
                            final_index_list.append(extended_name)
                        #If the length of the flight path index number is greater than 1, then we don't add a 0 to the front of it.
                        else:
                            extend= str(a)
                            final_index_list.append(extend)
                        #If the length of the flight time index number is equal to 1, then this statement will add a 0 to the front of it. This is used to make all index values two digits, so that we can have lists longer than 10.
                        if len(str(t))==1:
                            extend= str(t)
                            extended_name= extend.zfill(2)
                            final_index_list.append(extended_name)
                        #If the length of the flight time index number is greater than 1, then we don't add a 0 to the front of it.
                        else:
                            extend= str(t)
                            final_index_list.append(extend)
                        NewName1 = str(final_index_list[0]) + str(final_index_list[1]) + str(final_index_list[2]) + raster[34:36]
                        arcpy.CopyRaster_management(raster, NewName1)
                        VV_raster_list.append(NewName1)
                    #If the flight time is not in the time_list, then it will add it to that list and then add the indexed number of the flight time to the file name.
                    else:
                        a= flight_list.index(raster[7:12])
                        i= date_list.index(raster[23:29])
                        time_list.append(raster[20:22])
                        t= time_list.index(raster[20:22])
                        #If the length of the flight date index number is equal to 1, then this statement will add a 0 to the front of it. This is used to make all index values two digits, so that we can have lists longer than 10.
                        if len(str(i))==1:
                            extend=str(i)
                            extended_name= extend.zfill(2)
                            final_index_list.append(extended_name)
                        #If the length of the flight date index number is greater than 1, then we don't add a 0 to the front of it.
                        else:
                            extend= str(i)
                            final_index_list.append(extend)
                        #If the length of the flight path index number is equal to 1, then this statement will add a 0 to the front of it. This is used to make all index values two digits, so that we can have lists longer than 10.
                        if len(str(a))==1:
                            extend= str(a)
                            extended_name= extend.zfill(2)
                            final_index_list.append(extended_name)
                        #If the length of the flight path index number is greater than 1, then we don't add a 0 to the front of it.
                        else:
                            extend= str(a)
                            final_index_list.append(extend)
                        #If the length of the flight time index number is equal to 1, then this statement will add a 0 to the front of it. This is used to make all index values two digits, so that we can have lists longer than 10.
                        if len(str(t))==1:
                            extend= str(t)
                            extended_name= extend.zfill(2)
                            final_index_list.append(extended_name)
                        #If the length of the flight time index number is greater than 1, then we don't add a 0 to the front of it.
                        else:
                            extend= str(t)
                            final_index_list.append(extend)
                        NewName1 = str(final_index_list[0]) + str(final_index_list[1]) + str(final_index_list[2]) + raster[34:36]
                        arcpy.CopyRaster_management(raster, NewName1)
                        VV_raster_list.append(NewName1)
                        
                #If the flight path is not in the flight_list, then it will add it to that list and then add the indexed number of the flight path to the file name.
                else:
                    
                    #If the flight time is in the time_list then it will add the indexed number of the flight time to the file name.
                    if raster[20:22] in time_list:
                        i= date_list.index(raster[23:29])
                        flight_list.append(raster[7:12])
                        a=flight_list.index(raster[7:12])
                        t= time_list.index(raster[20:22])
                        #If the length of the flight date index number is equal to 1, then this statement will add a 0 to the front of it. This is used to make all index values two digits, so that we can have lists longer than 10.
                        if len(str(i))==1:
                            extend=str(i)
                            extended_name= extend.zfill(2)
                            final_index_list.append(extended_name)
                        #If the length of the flight date index number is greater than 1, then we don't add a 0 to the front of it.
                        else:
                            extend= str(i)
                            final_index_list.append(extend)
                        #If the length of the flight path index number is equal to 1, then this statement will add a 0 to the front of it. This is used to make all index values two digits, so that we can have lists longer than 10.
                        if len(str(a))==1:
                            extend= str(a)
                            extended_name= extend.zfill(2)
                            final_index_list.append(extended_name)
                        #If the length of the flight path index number is greater than 1, then we don't add a 0 to the front of it.
                        else:
                            extend= str(a)
                            final_index_list.append(extend)
                        #If the length of the flight time index number is equal to 1, then this statement will add a 0 to the front of it. This is used to make all index values two digits, so that we can have lists longer than 10.
                        if len(str(t))==1:
                            extend= str(t)
                            extended_name= extend.zfill(2)
                            final_index_list.append(extended_name)
                        #If the length of the flight time index number is greater than 1, then we don't add a 0 to the front of it.
                        else:
                            extend= str(t)
                            final_index_list.append(extend)
                        NewName1 = str(final_index_list[0]) + str(final_index_list[1]) + str(final_index_list[2]) + raster[34:36]
                        arcpy.CopyRaster_management(raster, NewName1)
                        VV_raster_list.append(NewName1)
                    #If the flight time is not in the time_list, then it will add it to that list and then add the indexed number of the flight time to the file name.
                    else:
                        i= date_list.index(raster[23:29])
                        flight_list.append(raster[7:12])
                        a=flight_list.index(raster[7:12])
                        time_list.append(raster[20:22])
                        t= time_list.index(raster[20:22])
                        #If the length of the flight date index number is equal to 1, then this statement will add a 0 to the front of it. This is used to make all index values two digits, so that we can have lists longer than 10.
                        if len(str(i))==1:
                            extend=str(i)
                            extended_name= extend.zfill(2)
                            final_index_list.append(extended_name)
                        #If the length of the flight date index number is greater than 1, then we don't add a 0 to the front of it.
                        else:
                            extend= str(i)
                            final_index_list.append(extend)
                        #If the length of the flight path index number is equal to 1, then this statement will add a 0 to the front of it. This is used to make all index values two digits, so that we can have lists longer than 10.
                        if len(str(a))==1:
                            extend= str(a)
                            extended_name= extend.zfill(2)
                            final_index_list.append(extended_name)
                        #If the length of the flight path index number is greater than 1, then we don't add a 0 to the front of it.
                        else:
                            extend= str(a)
                            final_index_list.append(extend)
                        #If the length of the flight time index number is equal to 1, then this statement will add a 0 to the front of it. This is used to make all index values two digits, so that we can have lists longer than 10.
                        if len(str(t))==1:
                            extend= str(t)
                            extended_name= extend.zfill(2)
                            final_index_list.append(extended_name)
                        #If the length of the flight time index number is greater than 1, then we don't add a 0 to the front of it.
                        else:
                            extend= str(t)
                            final_index_list.append(extend)
                        NewName1 = str(final_index_list[0]) + str(final_index_list[1]) + str(final_index_list[2]) + raster[34:36]
                        arcpy.CopyRaster_management(raster, NewName1)
                        VV_raster_list.append(NewName1)
            #If the flight date is not in the date_list, then it will add it to the list and then add the indexed number of the flight date to the file name.            
            else:
                #If the flight time is in the time_list then it will add the indexed number of the flight time to the file name.
                if raster[7:12] in flight_list:
                    #If the flight time is in the time_list then it will add the indexed number of the flight time to the file name.
                    if raster[20:22] in time_list:
                        date_list.append(raster[23:29])
                        i= date_list.index(raster[23:29])
                        a= flight_list.index(raster[7:12])
                        t= time_list.index(raster[20:22])
                        #If the length of the flight date index number is equal to 1, then this statement will add a 0 to the front of it. This is used to make all index values two digits, so that we can have lists longer than 10.
                        if len(str(i))==1:
                            extend=str(i)
                            extended_name= extend.zfill(2)
                            final_index_list.append(extended_name)
                        #If the length of the flight date index number is greater than 1, then we don't add a 0 to the front of it.
                        else:
                            extend= str(i)
                            final_index_list.append(extend)
                        #If the length of the flight path index number is equal to 1, then this statement will add a 0 to the front of it. This is used to make all index values two digits, so that we can have lists longer than 10.
                        if len(str(a))==1:
                            extend= str(a)
                            extended_name= extend.zfill(2)
                            final_index_list.append(extended_name)
                        #If the length of the flight path index number is greater than 1, then we don't add a 0 to the front of it.
                        else:
                            extend= str(a)
                            final_index_list.append(extend)
                        #If the length of the flight time index number is equal to 1, then this statement will add a 0 to the front of it. This is used to make all index values two digits, so that we can have lists longer than 10.
                        if len(str(t))==1:
                            extend= str(t)
                            extended_name= extend.zfill(2)
                            final_index_list.append(extended_name)
                        #If the length of the flight time index number is greater than 1, then we don't add a 0 to the front of it.
                        else:
                            extend= str(t)
                            final_index_list.append(extend)
                        NewName1 = str(final_index_list[0]) + str(final_index_list[1]) + str(final_index_list[2]) + raster[34:36]
                        arcpy.CopyRaster_management(raster, NewName1)
                        VV_raster_list.append(NewName1)
                    #If the flight time is not in the time_list, then it will add it to that list and then add the indexed number of the flight time to the file name.
                    else:
                        date_list.append(raster[23:29])
                        i= date_list.index(raster[23:29])
                        a= flight_list.index(raster[7:12])
                        time_list.append(raster[20:22])
                        t= time_list.index(raster[20:22])
                        #If the length of the flight date index number is equal to 1, then this statement will add a 0 to the front of it. This is used to make all index values two digits, so that we can have lists longer than 10.
                        if len(str(i))==1:
                            extend=str(i)
                            extended_name= extend.zfill(2)
                            final_index_list.append(extended_name)
                        #If the length of the flight date index number is greater than 1, then we don't add a 0 to the front of it.
                        else:
                            extend= str(i)
                            final_index_list.append(extend)
                        #If the length of the flight path index number is equal to 1, then this statement will add a 0 to the front of it. This is used to make all index values two digits, so that we can have lists longer than 10.
                        if len(str(a))==1:
                            extend= str(a)
                            extended_name= extend.zfill(2)
                            final_index_list.append(extended_name)
                        #If the length of the flight path index number is greater than 1, then we don't add a 0 to the front of it.
                        else:
                            extend= str(a)
                            final_index_list.append(extend)
                        #If the length of the flight time index number is equal to 1, then this statement will add a 0 to the front of it. This is used to make all index values two digits, so that we can have lists longer than 10.
                        if len(str(t))==1:
                            extend= str(t)
                            extended_name= extend.zfill(2)
                            final_index_list.append(extended_name)
                        #If the length of the flight time index number is greater than 1, then we don't add a 0 to the front of it.
                        else:
                            extend= str(t)
                            final_index_list.append(extend)
                        NewName1 = str(final_index_list[0]) + str(final_index_list[1]) + str(final_index_list[2]) + raster[34:36]
                        arcpy.CopyRaster_management(raster, NewName1)
                        VV_raster_list.append(NewName1)
                        
                #If the flight path is not in the flight_list, then it will add it to that list and then add the indexed number of the flight path to the file name.
                else:
                    #If the flight time is in the time_list then it will add the indexed number of the flight time to the file name.
                    if raster[20:22] in time_list:
                        date_list.append(raster[23:29])
                        i= date_list.index(raster[23:29])
                        flight_list.append(raster[7:12])
                        a=flight_list.index(raster[7:12])
                        t= time_list.index(raster[20:22])
                        #If the length of the flight date index number is equal to 1, then this statement will add a 0 to the front of it. This is used to make all index values two digits, so that we can have lists longer than 10.
                        if len(str(i))==1:
                            extend=str(i)
                            extended_name= extend.zfill(2)
                            final_index_list.append(extended_name)
                        #If the length of the flight date index number is greater than 1, then we don't add a 0 to the front of it.
                        else:
                            extend= str(i)
                            final_index_list.append(extend)
                        #If the length of the flight path index number is equal to 1, then this statement will add a 0 to the front of it. This is used to make all index values two digits, so that we can have lists longer than 10.
                        if len(str(a))==1:
                            extend= str(a)
                            extended_name= extend.zfill(2)
                            final_index_list.append(extended_name)
                        #If the length of the flight path index number is greater than 1, then we don't add a 0 to the front of it.
                        else:
                            extend= str(a)
                            final_index_list.append(extend)
                        #If the length of the flight time index number is equal to 1, then this statement will add a 0 to the front of it. This is used to make all index values two digits, so that we can have lists longer than 10.
                        if len(str(t))==1:
                            extend= str(t)
                            extended_name= extend.zfill(2)
                            final_index_list.append(extended_name)
                        #If the length of the flight time index number is greater than 1, then we don't add a 0 to the front of it.
                        else:
                            extend= str(t)
                            final_index_list.append(extend)
                        NewName1 = str(final_index_list[0]) + str(final_index_list[1]) + str(final_index_list[2]) + raster[34:36]
                        arcpy.CopyRaster_management(raster, NewName1)
                        VV_raster_list.append(NewName1)
                    #If the flight time is not in the time_list, then it will add it to that list and then add the indexed number of the flight time to the file name.
                    else:
                        date_list.append(raster[23:29])
                        i= date_list.index(raster[23:29])
                        flight_list.append(raster[7:12])
                        a=flight_list.index(raster[7:12])
                        time_list.append(raster[20:22])
                        t= time_list.index(raster[20:22])
                        #If the length of the flight date index number is equal to 1, then this statement will add a 0 to the front of it. This is used to make all index values two digits, so that we can have lists longer than 10.
                        if len(str(i))==1:
                            extend=str(i)
                            extended_name= extend.zfill(2)
                            final_index_list.append(extended_name)
                        #If the length of the flight date index number is greater than 1, then we don't add a 0 to the front of it.
                        else:
                            extend= str(i)
                            final_index_list.append(extend)
                        #If the length of the flight path index number is equal to 1, then this statement will add a 0 to the front of it. This is used to make all index values two digits, so that we can have lists longer than 10.
                        if len(str(a))==1:
                            extend= str(a)
                            extended_name= extend.zfill(2)
                            final_index_list.append(extended_name)
                        #If the length of the flight path index number is greater than 1, then we don't add a 0 to the front of it.
                        else:
                            extend= str(a)
                            final_index_list.append(extend)
                        #If the length of the flight time index number is equal to 1, then this statement will add a 0 to the front of it. This is used to make all index values two digits, so that we can have lists longer than 10.
                        if len(str(t))==1:
                            extend= str(t)
                            extended_name= extend.zfill(2)
                            final_index_list.append(extended_name)
                        #If the length of the flight time index number is greater than 1, then we don't add a 0 to the front of it.
                        else:
                            extend= str(t)
                            final_index_list.append(extend)
                        NewName1 = str(final_index_list[0]) + str(final_index_list[1]) + str(final_index_list[2]) + raster[34:36]
                        arcpy.CopyRaster_management(raster, NewName1)
                        VV_raster_list.append(NewName1)
                        
arcpy.AddMessage("Raster lists compiled.")
#For loop that searchs through the HH_raster_list. 
for rast in HH_raster_list:
    VV_grd= VV_raster_list[x]
    HH_grd= HH_raster_list[x]
    VV_srt= "a" + str(VV_grd[0:7])
    HH_srt= "a" + str(HH_grd[0:7])

    #Extract by Mask
    arcpy.gp.ExtractByMask_sa(VV_grd, Buffer_Shapefile, VV_srt)
    arcpy.gp.ExtractByMask_sa(HH_grd, Buffer_Shapefile, HH_srt)
    arcpy.AddMessage("Extraction by mask complete.")
    
    #Divide
    Divided="b" + str(VV_grd[0:6])
    arcpy.gp.Divide_sa(VV_srt, HH_srt, Divided)
    arcpy.AddMessage("Divide complete.")
    
    #Low Pass Filter
    Filtered= str(Divided) + str(x)
    arcpy.gp.Filter_sa(Divided, Filtered, "LOW", "DATA")
    arcpy.AddMessage("Low pass filter complete.")
    
    #Unsupervised Classification
    Classified= Divided
    Output_signature_file= "Scrap.gsg"
    outUnsupervised = IsoClusterUnsupervisedClassification(Filtered, 12, 20, 10, Output_signature_file)
    outUnsupervised.save(Classified)
    arcpy.AddMessage("Unsupervised classification complete.")
    
    #Reclassify
    Reclass2= "Reclass"
    outReclass2= Reclassify(Classified, "Value", RemapRange([[1,10,0],[10,12,1]]))
    outReclass2.save(Reclass2)

    #If a mask is used, then this if statement will subtract the mask from the Reclassified raster.
    if arcpy.Exists(Mask):
        #Apply Mask
        outMinus1= Minus(Reclass2, Mask)
        outMinus1.save("Minus")
        arcpy.AddMessage("Mask application complete.")

        #Reclassify
        Reclass3= "Reclass3"
        outReclass3= Reclassify("Minus", "Value", RemapRange([[-1,0.1,0],[0.1,1,1]]))
        outReclass3.save(Reclass3)

        #Region group.
        Region_Group = RegionGroup(Reclass3)
        Region_Group.save("Region_Group2")

        #Conditional
        arcpy.AddMessage(str(x))
        Conditional= Con("Region_Group2", "0", "1", z)
        Conditional.save("Con_O")

        #Take out the Conditional from the reclass
        outMinus = Minus(Reclass3, "Con_O")
        outMinus.save("Minus1")

        #Reclassify
        Reclass4= "Reclass4"
        outReclass4= Reclassify("Minus1", "Value", RemapRange([[-1,0,"NoData"],[0,1,1]]))
        outReclass4.save(Reclass4)
    
        #Raster to Polygon
        Polygon= "Polygon.shp"
        arcpy.RasterToPolygon_conversion(Reclass4, Polygon, "NO_SIMPLIFY", "VALUE")
    
        #Make Feature Layer
        arcpy.MakeFeatureLayer_management(Polygon, "Del.lyr")
    
        #Layer To KML
        FlightDate= int(Divided[1:3])
        FlightPath= int(Divided[3:5])
        FlightTime= int(Divided[5:7])
        
        KML_File= Frequency_folder + "/" + str(flight_list[FlightPath]) + "_" + str(date_list[FlightDate]) + "_" + str(time_list[FlightTime]) + ".kmz"
        Final_Layer= str(flight_list[FlightPath]) + "_" + str(date_list[FlightDate]) + "_" + str(time_list[FlightTime])
        arcpy.MakeFeatureLayer_management("Del.lyr", Final_Layer)

        #Apply Symbology From Layer
        arcpy.ApplySymbologyFromLayer_management(Final_Layer, Symbology_Layer)
        arcpy.LayerToKML_conversion(Final_Layer, KML_File, "1", "false", "DEFAULT", "1024", "96", "CLAMPED_TO_GROUND")
        arcpy.AddMessage("KMZ file successfully created.")
        
        #Reclassify for Frequency Tool
        FlightDate= int(Divided[1:3])
        FlightPath= int(Divided[3:5])
        FlightTime= int(Divided[5:7])
    
        Reclass1= Frequency_folder + "/" + str(flight_list[FlightPath]) + str(date_list[FlightDate]) + str(time_list[FlightTime])
        outReclass1= Reclassify("Minus1", "Value", RemapRange([[-1,0,0],[0,1,1]]))
        outReclass1.save(Reclass1)
        arcpy.AddMessage("Raster file successfully created.")
        
        #Add one to the iteration counter.
        x= x+1
        
    #If no mask is used, then the tool will skip the "Apply Mask" step.
    else:
        #Region group.
        Region_Group = RegionGroup(Reclass2)
        Region_Group.save("Region_Group2")

        #Conditional
        Conditional= Con("Region_Group2", "0", "1", z)
        Conditional.save("Con_O")

        #Take out the Conditional from the reclass
        outMinus = Minus(Reclass2, "Con_O")
        outMinus.save("Minus1")

        #Reclassify
        Reclass4= "Reclass4"
        outReclass4= Reclassify("Minus1", "Value", RemapRange([[-1,0,"NoData"],[0,1,1]]))
        outReclass4.save(Reclass4)
    
        #Raster to Polygon
        Polygon= "Polygon.shp"
        arcpy.RasterToPolygon_conversion(Reclass4, Polygon, "NO_SIMPLIFY", "VALUE")
        
        #Make Feature Layer
        arcpy.MakeFeatureLayer_management(Polygon, "Del.lyr")
    
        #Layer To KML
        FlightDate= int(Divided[1:3])
        FlightPath= int(Divided[3:5])
        FlightTime= int(Divided[5:7])
    
        KML_File= Frequency_folder + "/" + str(flight_list[FlightPath]) + "_" + str(date_list[FlightDate]) + "_" + str(time_list[FlightTime]) + ".kmz"
        Final_Layer= str(flight_list[FlightPath]) + "_" + str(date_list[FlightDate]) + "_" + str(time_list[FlightTime])

        #Rename "Del.lyr"
        arcpy.MakeFeatureLayer_management("Del.lyr", Final_Layer)

        #Apply Symbology From Layer
        arcpy.ApplySymbologyFromLayer_management(Final_Layer, Symbology_Layer)
        
        arcpy.LayerToKML_conversion(Final_Layer, KML_File, "1", "false", "DEFAULT", "1024", "96", "CLAMPED_TO_GROUND")
        arcpy.AddMessage("KMZ file successfully created.")

        #Reclassify for Frequency Tool
        FlightDate= int(Divided[1:3])
        FlightPath= int(Divided[3:5])
        FlightTime= int(Divided[5:7])
        
        Reclass1= Frequency_folder + "/" + str(flight_list[FlightPath]) + str(date_list[FlightDate]) + str(time_list[FlightTime])
        outReclass1= Reclassify("Minus1", "Value", RemapRange([[-1,0,0],[0,1,1]]))
        outReclass1.save(Reclass1)
        arcpy.AddMessage("Raster file successfully created.")
        
        #Add one to the iteration counter.
        x= x+1

