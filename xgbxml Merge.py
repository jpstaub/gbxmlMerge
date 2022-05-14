# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# todo: implement xgbxml 

# import packages
from lxml import etree
from xgbxml import get_parser
import matplotlib.pyplot as plt
from copy import copy

# file gui
from tkinter import ttk

from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog

Tk().withdraw()

# define file variables
fpa = "./Input gbXML/TrueNorth 000/gbXML A_Geometry.xml"
fpb = "./Input gbXML/TrueNorth 000/gbXML B_Opening.xml"
fpo = "./Output gbXML/xgbxml C_Geometry-Opening_TrueNorth 000.xml"

# define file variables with gui
# fpa = filedialog.askopenfilename(title="gbXML Without Openings", filetypes=[("xml","*.xml")])
# fpb = filedialog.askopenfilename(title="gbXML With Openings", filetypes=[("xml","*.xml")])
# fpo = filedialog.asksaveasfilename(defaultextension='.xml', filetypes=[("xml","*.xml")])

# uses xgbxml to generate a lxml parser to read gxXML version 0.37
parser=get_parser(version='0.37')

# opens the file using the lxml parser
tree_A = etree.parse(fpa,parser)
gbxml_A = tree_A.getroot()

# renders the gbXML etree
ax = gbxml_A.Campus.render()
ax.figure.set_size_inches(8, 8)
ax.set_title('gbXML A_Geometry.xml')
plt.show()

# opens the file using the lxml parser
tree_B = etree.parse(fpb,parser)
gbxml_B = tree_B.getroot()

# renders the gbXML etree
ax = gbxml_B.Campus.render()
ax.figure.set_size_inches(8, 8)
ax.set_title('gbXML B_Openings.xml')
plt.show()

# creates a copy of gbxml_A which is named gbxml_C
gbxml_C = copy(gbxml_A)
etree_C = etree.ElementTree(gbxml_C)

# find openings in gbxml_B and merge with gbxml_C
openings = list(gbxml_B.Campus.Surfaces.Openings)
for su in gbxml_C.Campus.Surfaces:
    for opening in openings:
        try:
            su.copy_opening(opening,tolerance=0.01)
            openings.remove(opening)
            break
        except ValueError:
            pass

# renders the gbXML etree
ax = gbxml_C.Campus.render()
ax.figure.set_size_inches(8, 8)
ax.set_title('gbXML C_Composite.xml')
plt.show()

# writes the gbXML_C etree to a local file
etree_C.write(fpo, pretty_print=True)


