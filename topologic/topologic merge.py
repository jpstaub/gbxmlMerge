# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#Todo: implement Topologic (https://topologic.app/user_doc :: Topologic:Utilities:FaceUtility:IsInside) to detect containment of opening vertex in surface faces.

# import packages
from lxml import etree
from xgbxml import get_parser
import matplotlib.pyplot as plt
from copy import copy
# import geometer as gm
# import numpy as np
import topologicpy as tp


# file gui
from tkinter import ttk

from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog

Tk().withdraw()

# define file variables
fpa = "./Input/gbXML A_Geometry.xml"
fpb = "./Input/gbXML B_Opening.xml"
fpo = "./Output/gbxml C_GeometryOpening.xml"

# # define file variables with gui
# fpa = filedialog.askopenfilename(title="gbXML Without Openings", filetypes=[("xml","*.xml")])
# fpb = filedialog.askopenfilename(title="gbXML With Openings", filetypes=[("xml","*.xml")])
# fpo = filedialog.asksaveasfilename(defaultextension='.xml', filetypes=[("xml","*.xml")])

# uses xgbxml to generate a lxml parser to read gxXML version 0.37
parser=get_parser(version='0.37')

# opens the file using the lxml parser
tree_A = etree.parse(fpa,parser)
gbxml_A = tree_A.getroot()

# # renders the gbXML etree
# ax = gbxml_A.Campus.render()
# ax.figure.set_size_inches(8, 8)
# ax.set_title('gbXML A_Geometry.xml')
# plt.show()

# opens the file using the lxml parser
tree_B = etree.parse(fpb,parser)
gbxml_B = tree_B.getroot()

# # renders the gbXML etree
# ax = gbxml_B.Campus.render()
# ax.figure.set_size_inches(8, 8)
# ax.set_title('gbXML B_Openings.xml')
# plt.show()

# creates a copy of gbxml_A which is named gbxml_C
gbxml_C = copy(gbxml_A)
etree_C = etree.ElementTree(gbxml_C)

# topologicpy functional development & test sandbox
# dpt = (86.2243728, 124.2768145, 3.0)
# vert = tp.topologic.Vertex.ByCoordinates(dpt[0],dpt[1],dpt[2])
# coord = tp.topologic.Vertex.Coordinates(vert)

# generate opening vertices (ov)
# l = len(gbxml_B.Campus.Surfaces.Openings)
ov = []
for opening in gbxml_B.Campus.Surfaces.Openings:
    opt = opening.PlanarGeometry.PolyLoop.CartesianPoint.get_coordinates()
    ov.append(tp.topologic.Vertex.ByCoordinates(opt[0],opt[1],opt[2]))
    
def faceByVertices(vertices):
    vertices
    edges = []
    for i in range(len(vertices)-1):
        v1 = vertices[i]
        v2 = vertices[i+1]
        try:
            e = tp.Edge.ByStartVertexEndVertex(v1, v2)
            if e:
                edges.append(e)
        except:
            continue

    v1 = vertices[-1]
    v2 = vertices[0]
    try:
        e = tp.Edge.ByStartVertexEndVertex(v1, v2)
        if e:
            edges.append(e)
    except:
        pass
    if len(edges) > 3:
        c = tp.Cluster.ByTopologies(edges, False)
        w = c.SelfMerge()
        if w.Type() == tp.Wire.Type() and w.IsClosed():
            f = tp.Face.ByExternalBoundary(w)
        else:
            raise Exception("Error: Could not get a valid wire")
    else:
        raise Exception("Error: could not get a valid number of edges")
    return f
    
# generate surface faces (sf)
sf = []
for surface in gbxml_C.Campus.Surfaces:
    if surface.get_attribute('surfaceType') == 'ExteriorWall':
        sv = []
        # s = surface.PlanarGeometry.get_coordinates()
        for spt in surface.PlanarGeometry.get_coordinates():
            sv.append(tp.topologic.Vertex.ByCoordinates(spt[0],spt[1],spt[2]))
        print(sv)
        sf.append(faceByVertices(sv))

# # find openings in gbxml_B and merge with gbxml_C (Original - fail: counts down openings and prevents cycle of all openings)
# openings = list(gbxml_B.Campus.Surfaces.Openings)
# for su in gbxml_C.Campus.Surfaces:
#     for opening in openings:
#         try:
#             su.copy_opening(opening,tolerance=0.01)
#             openings.remove(opening)
#             break
#         except ValueError:
#             pass

# find openings in gbxml_B and merge with gbxml_C (Dev Attempt #1 - pass: cycles openings through all surfaces)
for opening in gbxml_B.Campus.Surfaces.Openings:
    for surface in gbxml_C.Campus.Surfaces:
        if surface.get_attribute('surfaceType') == 'ExteriorWall':
            try:
                surface.copy_opening(opening,tolerance=0.01)
                # openings.remove(opening)
                break
            except ValueError:
                pass
        
# # find openings in gbxml_B and merge with gbxml_C (Dev Attempt #2 - fail: does not cycle surface more than once)
# openings = list(gbxml_B.Campus.Surfaces.Openings)
# for su in gbxml_C.Campus.Surfaces:
#     for opening in openings:
#         try:
#             su.copy_opening(opening,tolerance=0.01)
#             # openings.remove(opening)
#             break
#         except ValueError:
#             pass        
          

# # renders the gbXML etree
# ax = gbxml_C.Campus.render()
# ax.figure.set_size_inches(8, 8)
# ax.set_title('gbXML C_Composite.xml')
# plt.show()

# writes the gbXML_C etree to a local file
# etree_C.write(fpo, pretty_print=True)


