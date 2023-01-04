# -*- coding: utf-8 -*-
"""
Spyder Editor

Merges two gbXML files exported from Revit. First gbXML based on Revit masses does not include openings.
Second gbXML based on Revit spaces includes openings. Openings within variable 'dist' parameter are
take from gbXML based on Revit spaces and merged with gbXML based on Revit masses.
"""


# Topologic on PyPi: https://test.pypi.org/project/topologicpy/


# import: modules
from lxml import etree
from xgbxml import get_parser
import matplotlib.pyplot as plt
from copy import copy
# import topologicpy.bin.topologic.topologic as tp
from topologicpy import topologic as tp # proven to be the most reliable method of importing 'topologic'


# print(dir(tp.FaceUtility)) # troubleshooting of topologic module path(s)


# import: gui modules
from tkinter import ttk
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
Tk().withdraw() # hides command line window


# # define: file variables: sandbox project
# fpa = "./topologic/Input/01_Simplified/Wall Interior/Simple Building_Separation Lines_Wall Interior_Mass.xml"
# fpb = "./topologic/Input/01_Simplified/Wall Interior/Simple Building_Separation Lines_Wall Interior_Space.xml"
# fpo = "./topologic/Output/01_Simplified/Simple Building_Separation Lines_Wall Interior.xml"


# define: file variables with gui
fpa = filedialog.askopenfilename(title="gbXML Without Openings", filetypes=[("xml","*.xml")])
fpb = filedialog.askopenfilename(title="gbXML With Openings", filetypes=[("xml","*.xml")])
fpo = filedialog.asksaveasfilename(defaultextension='.xml', filetypes=[("xml","*.xml")])


# set: distance tolerance of opening from surface in gbXML length units (typically the thickness of the roof or wall)
dist = 1.0


# use: xgbxml to generate a lxml parser / read: gbXML version from input file
tree_parser=etree.parse(fpa)
gbxml=tree_parser.getroot()
parser=get_parser(version=gbxml.attrib['version'])
# parser=get_parser(version='0.37')


# open: the file using the lxml parser
tree_A = etree.parse(fpa,parser)
gbxml_A = tree_A.getroot()


# # render: the gbXML etree
# ax = gbxml_A.Campus.render()
# ax.figure.set_size_inches(8, 8)
# ax.set_title('gbXML A_Geometry.xml')
# plt.show()


# open: the file using the lxml parser
tree_B = etree.parse(fpb,parser)
gbxml_B = tree_B.getroot()


# # render: the gbXML etree
# ax = gbxml_B.Campus.render()
# ax.figure.set_size_inches(8, 8)
# ax.set_title('gbXML B_Openings.xml')
# plt.show()


# make: a copy of gbxml_A named gbxml_C
gbxml_C = copy(gbxml_A)
etree_C = etree.ElementTree(gbxml_C)


# define: topologicpy faceByVertices (Wassim Jabi) - 27MAY22
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
    # print("V1:", v1.X(), v1.Y(), v1.Z())
    # print("V2:", v2.X(), v2.Y(), v2.Z())
    try:
        e = tp.Edge.ByStartVertexEndVertex(v1, v2)
        if e:
            edges.append(e)
    except:
        print("Edge creation failed!")
        pass
    # print("I managed to create",len(edges),"edges")
    if len(edges) >= 3:
        c = tp.Cluster.ByTopologies(edges, False)
        w = c.SelfMerge()
        if w.Type() == tp.Wire.Type() and w.IsClosed():
            f = tp.Face.ByExternalBoundary(w)
        else:
            raise Exception("Error: Could not get a valid wire")
    else:
        raise Exception("Error: could not get a valid number of edges")
    return f


# get: gbxml_B openings (ops)  
# make: Topologic opening centroids from gbxml_B openings (ocs)
ops = []
ocs = []
for op in gbxml_B.Campus.Surfaces.Openings:
    ops.append(op)
    o = []
    for c in op.PlanarGeometry.get_coordinates():
        o.append(tp.Vertex.ByCoordinates(c[0],c[1],c[2]))
    ocs.append(tp.Topology.Centroid(faceByVertices(o)))
    

# get: gbxml_C exterior surfaces (exsu)
# make: Topologic suface faces (sfs) from gbxml_C surfaces
exsu = []
sfs = []
for su in gbxml_C.Campus.Surfaces:
    if su.get_attribute('surfaceType') in ['ExteriorWall', 'Roof']:
    # if su.get_attribute('surfaceType') in ['Roof']:        
        exsu.append(su)
        s = []
        for c in su.PlanarGeometry.get_coordinates():
            s.append(tp.Vertex.ByCoordinates(c[0],c[1],c[2]))
        sfs.append(faceByVertices(s))


# test: gbxml_B Topologic opening centroid (ocs) IsInside(face,point,tolerance) of gbxml_C Topologic surface face (sfs) (vin)
vin = []
for oc in ocs:
    r = []
    for sf in sfs:
        r.append(tp.FaceUtility.IsInside(sf,oc,dist))
    vin.append(r)
    
   
# # qa: count number of true responses per opening vertex
# count = []
# for v in vin:
#     count.append(v.count(True))
    
    
# get: indices of gbxml_C surfaces with gbxml_B opening centroid isinside (sfoc)
sfoc = []
for v in vin:
    if True in v:
        sfoc.append(v.index(True))
    else:
        sfoc.append(False)       

       
# insert: gbxml_B opening into gbxml_C surface object if opening within variable 'dist' parameter
i = 0
for sf in sfoc:
    if sf==False:
        i+=1
    else:
        try:
            exsu[sf].insert(3, exsu[sf].copy_opening(ops[i],tolerance=dist)) # copy_opening is xgbxml method
            i+=1
        except ValueError:
            print('Caught ValueError. Check opening: ' + ops[i].Name.text + '.')            
            i+=1
        except Exception:
            print('Caught Exception. Check opening: ' + ops[i].Name.text + '.')            
            i+=1


# render: the gbXML etree
ax = gbxml_C.Campus.render()
ax.figure.set_size_inches(8, 8)
ax.set_title('gbXML C_Composite.xml')
plt.show()


# write: the gbXML_C etree to a local file
etree_C.write(fpo, pretty_print=True)
