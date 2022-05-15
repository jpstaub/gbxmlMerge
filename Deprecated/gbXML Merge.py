# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#Todo: implement geometer (https://geometer.readthedocs.io/en/stable :: geometer.shapes module : class geometer.shapes.Polygon.contains) to detect containment of opening centroids in surface polygons.

import xml.etree.ElementTree as ET

from tkinter import ttk

from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog

Tk().withdraw()


filenameOpenings = filedialog.askopenfilename(title="gbXML With Openings", filetypes=[("xml","*.xml")])
filenameGeometry = filedialog.askopenfilename(title="gbXML Without Openings", filetypes=[("xml","*.xml")])

filenameOut = filedialog.asksaveasfilename(defaultextension='.xml', filetypes=[("xml","*.xml")])

#Files
# gbxmlWithOpenings = "Z:/CAD/Autodesk/RVT/Dynamo/Dynamo 2_X/dev/11_AutomatedBuildingEnergyModel/Output/Revit/Spaces/Simple Building_Separation Lines_22-03-20/gbXML A_Openings.xml"
# gbxmlWithGeometry = "Z:/CAD/Autodesk/RVT/Dynamo/Dynamo 2_X/dev/11_AutomatedBuildingEnergyModel/Output/Revit/EAM/Simple Building_Separation Lines_22-03-20/gbXML B_Geometry.xml"
# gbxmlOut = "out.xml"


gbxmlWithOpenings = filenameOpenings
gbxmlWithGeometry = filenameGeometry

gbxmlOut = filenameOut

#namespaces
ns = {'gbxml':'http://www.gbxml.org/schema'}


#Registers namespace so that an additional namespace tag is not written to elements
ET.register_namespace('','http://www.gbxml.org/schema')


#Parse gbXML files
openingDataTree = ET.parse(gbxmlWithOpenings)
geometryDataTree = ET.parse(gbxmlWithGeometry)


#Set root
openingRoot = openingDataTree.getroot()
geometryRoot = geometryDataTree.getroot()


#Declare dictionaries
openingPoints = {}
openings = {}
cleanWalls = {}
geometryPoints = {}
matchedWall = {}


#Make dictionary of cartesian points of ExteriorWall w/Openings with wall 'id' as key
for openingExteriorWall in openingRoot.findall(".//gbxml:Opening/..[@surfaceType='ExteriorWall']", ns):
    matchPoint = []
    for cartesianPoint in openingExteriorWall.find(".//gbxml:PolyLoop/gbxml:CartesianPoint[2]", ns):
        matchPoint.append(cartesianPoint.text)
    # join CartesianPoint values into a single value for comparison
    openingPoints[openingExteriorWall.get('id')] = ''.join(matchPoint)


#Make dictionary of Openings with wall 'id' as key
for openingExteriorWall in openingRoot.findall(".//gbxml:Opening/..[@surfaceType='ExteriorWall']", ns):
    openingList = []
    for opening in openingExteriorWall.findall(".//gbxml:Opening", ns):
        new_opening_id = opening.get('id') + 'M'
        opening.set('id', new_opening_id)
        openingList.append(opening)
    # join CartesianPoint values into a single value for comparison
    openings[openingExteriorWall.get('id')] = openingList


#Make dictionary of walls and cartesian points of ExteriorWall w/o Openings with wall 'id' as key   
for exteriorWall in geometryRoot.findall(".//gbxml:Surface/.[@surfaceType='ExteriorWall']", ns):
    cleanWalls[exteriorWall.get('id')] = exteriorWall
    matchPoint = []
    for cartesianPoint in exteriorWall.find(".//gbxml:PolyLoop/gbxml:CartesianPoint[2]", ns):
        matchPoint.append(cartesianPoint.text)
    # join CartesianPoint values into a single value for comparison 
    geometryPoints[exteriorWall.get('id')] = ''.join(matchPoint)

geometryPoints_key_list = list(geometryPoints.keys())
geometryPoints_val_list = list(geometryPoints.values())

    
#Make dictionary of matching wall cartesian points with ExteriorWall w/Opening 'id' as key
for point in openingPoints:
    position = geometryPoints_val_list.index(openingPoints.get(point))
    matchedWall[point] = geometryPoints_key_list[position]

        
#Place openings in ExteriorWall w/o Opening
for wall in matchedWall:
    wallSurface = cleanWalls.get(matchedWall.get(wall))
    elements = openings.get(wall)
    for element in elements:
        wallSurface.insert(3, element)


geometryDataTree.write(gbxmlOut, encoding='UTF-8', xml_declaration=True)

