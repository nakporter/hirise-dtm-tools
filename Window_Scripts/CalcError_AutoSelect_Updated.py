#######################################################################
# Program: CalcError_AutoSelect.py                                    #
# Author: Donna Viola (dviola@lpl.arizona.edu)                        #
# Date: April 15, 2013                                                #
#                                                                     #
# This program will take an input DTM and the accompanying MOLA       #
# tracks to extract elevation values, calculate the error, and export #
# a feature class containing only valid points in the DTM.            #
#######################################################################

#Import arcpy and relevant modules
import arcpy
import os, sys 
from arcpy import env
arcpy.CheckOutExtension("Spatial")
from arcpy.sa import *

#Collect user inputs
inTracks = arcpy.GetParameterAsText(0)
folder = arcpy.GetParameterAsText(1)
inDTM = arcpy.GetParameterAsText(2)
arcpy.AddMessage("Starting...")

#Set location of symbology layer. 
symbologyLocation = "C:\scripts\ErrorMapping\MOLAsymbology.lyr"


#this turns on overwrite 
arcpy.env.overwriteOutput = True

#Create a geodatabase workspace
#checks to see if the geodatabase has already been created, 
#if it has it will then just take the geotiff name and add it as an extention 


if os.path.exists(folder+"\Geodatabase.gdb"):
	arcpy.AddMessage("Im using this check")#for debugging purposes

	env.workspace = "Geodatabase.gdb"#workspace being defined
	
	#this creates the geotiff extension
	temp=os.path.basename(inDTM)
	mapName=str(inDTM[0:temp.index('.')])
	mapName=mapName.replace('-','_')

	
else:#If the geodatabase workspace has not been created it will then create and name the workspace to Geodatabase
	
	arcpy.AddMessage("Creating file GDB...")
	gdb = arcpy.CreateFileGDB_management(folder, "Geodatabase")
	gdbName = str(gdb)
	env.workspace = gdbName
	
	#this creates the geotiff extension
	temp=os.path.basename(inDTM)
	mapName=str(inDTM[0:temp.index('.')])
	mapName=mapName.replace('-','_')
	
	
	
#Extract DTM values to selection layer points

arcpy.AddMessage("Extracting raster points...")
rasterPoints = ExtractValuesToPoints(inTracks, inDTM, "RasterPts_"+mapName)

#Create new layer using only valid points

arcpy.AddMessage("Selecting and exporting valid points...")
validPts = arcpy.Select_analysis(rasterPoints, "ValidPts_"+mapName, "\"RASTERVALU\" > -9999") 

#Add "Error" field and calculate values
arcpy.AddMessage("Calculating error...")
arcpy.AddField_management(validPts, "Error", "DOUBLE")
arcpy.CalculateField_management(validPts, "Error", "[topography] - [RASTERVALU]", "VB", "")

#Make feature layer and apply symbology
arcpy.AddMessage("Creating valid points layer and applying symbology...")
arcpy.MakeFeatureLayer_management(validPts, "validLayer_"+mapName)
arcpy.ApplySymbologyFromLayer_management("validLayer_"+mapName, symbologyLocation)

#Add extracted points layer to map
arcpy.AddMessage("Adding valid points layer to map...")
mxd = arcpy.mapping.MapDocument("CURRENT")
df = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]
addLayer = arcpy.mapping.Layer("validLayer_"+mapName)
arcpy.mapping.AddLayer(df, addLayer, "AUTO_ARRANGE")
arcpy.RefreshActiveView()
arcpy.RefreshTOC()

del addLayer
