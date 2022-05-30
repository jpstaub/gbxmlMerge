# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# Todo: implement Topologic (https://topologic.app/user_doc :: Topologic:Utilities:FaceUtility:IsInside) to detect containment of opening vertex in surface faces.
# Topologic on PyPi: https://test.pypi.org/project/topologicpy/


# import: modules
from lxml import etree
from xgbxml import get_parser
import matplotlib.pyplot as plt
from copy import copy
from topologicpy import topologic as tp # from 'foo' import 'bar': this syntax required for topologicpy functionality


# import: gui modules
from tkinter import ttk
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
Tk().withdraw() # hides command line window


# # define: file variables: sandbox project
# fpa = "./Input/01_Simplified/gbXML A_Geometry.xml"
# fpb = "./Input/01_Simplified/gbXML B_Opening_Multiple.xml"
# fpo = "./Output/01_Simplified/gbXML C_GeometryOpenings.xml"

# # define: file variables: production project
# fpa = "./Input/02_Production/22-013 Blue Star Kilbourne_Geometry.xml"
# fpb = "./Input/02_Production/22-013 Blue Star Kilbourne_Openings.xml"
# fpo = "./Output/02_Production/22-013 Blue Star Kilbourne_GeometryOpenings.xml"


# define: file variables with gui
fpa = filedialog.askopenfilename(title="gbXML Without Openings", filetypes=[("xml","*.xml")])
fpb = filedialog.askopenfilename(title="gbXML With Openings", filetypes=[("xml","*.xml")])
fpo = filedialog.asksaveasfilename(defaultextension='.xml', filetypes=[("xml","*.xml")])


# use: xgbxml to generate a lxml parser / read: gxXML version 0.37
parser=get_parser(version='0.37')


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


# make: a copy of gbxml_A which is named gbxml_C
gbxml_C = copy(gbxml_A)
etree_C = etree.ElementTree(gbxml_C)


# define: topologicpy faceByVertices (Wassim Jabi) - 27MAY
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

    
# make: opening centroids (ocs)
ocs = []
for op in gbxml_B.Campus.Surfaces.Openings:
    o = []
    for c in op.PlanarGeometry.get_coordinates():
        o.append(tp.Vertex.ByCoordinates(c[0],c[1],c[2]))
    ocs.append(tp.Topology.Centroid(faceByVertices(o)))


# make: surface faces (sfs)
sfs = []
for su in gbxml_A.Campus.Surfaces:
    # if surface.get_attribute('surfaceType') == 'ExteriorWall':
        s = []
        for c in su.PlanarGeometry.get_coordinates():
            s.append(tp.Vertex.ByCoordinates(c[0],c[1],c[2]))
        sfs.append(faceByVertices(s))


# test: opening vertex IsInside(face,point,tolerance) of surface face (vin)
vin = []
for oc in ocs:
    r = []
    for sf in sfs:
        r.append(tp.FaceUtility.IsInside(sf,oc,0.01))
    vin.append(r)
    
    
# # qa: count number of true responses per opening vertex
# count = []
# for v in vin:
#     count.append(v.count(True))
    
    
# get: indices of vertex isinside of surface face (ivif)
ivif = []
for v in vin:
    ivif.append(v.index(True))


# make: list of surface objects (suobs)
suobs = []
for i in ivif:
    suobs.append(gbxml_C.Campus.Surfaces[i])
    

# insert: opening into gbxml_C surface
i = 0
for op in gbxml_B.Campus.Surfaces.Openings:
    suobs[i].insert(3, op)
    i = i+1
     

# render: the gbXML etree
ax = gbxml_C.Campus.render()
ax.figure.set_size_inches(8, 8)
ax.set_title('gbXML C_Composite.xml')
plt.show()


# write: the gbXML_C etree to a local file
etree_C.write(fpo, pretty_print=True)


