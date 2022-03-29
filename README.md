# gbxmlMerge
Merge Openings in gbXML File A with Surfaces in gbXML File B to Surfaces with Openings in gbXML File C.

Purpose: This python script is meant to process full Revit gbXML input files in XML format:
		 (1) A geometry gbXML based on mass families without windows,
		 (2) A Spaces gbXML based on detailed elements with windows.

Inputs:
1. Revit gbXML files in XML format. File locations are chosen via a typical directory GUI.
2. Output file name and destination location via a typical directory GUI.


Outputs:
1. Geometry from gbXML based on mass families and Windows from gbXML based on Spaces.


Notes:
1. None


Functional Development & Test:
Windows 10
Anaconda / Spyder IDE / Python 3.8
