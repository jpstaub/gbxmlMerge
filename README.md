# gbxmlMerge
Merge 'Geometry' in gbXML File A with 'Openings' in gbXML File B to 'Geometry with Openings' in gbXML File C.

Purpose: This python script is meant to process full Revit gbXML input files in XML format:
1. A Geometry gbXML based on Mass families without windows,
2. An Openings gbXML based on Spaces from detailed elements with windows.

Inputs:
1. Revit gbXML files in XML format. File locations are chosen via a typical directory GUI.
2. Output file name and destination location via a typical directory GUI.


Outputs:
1. Composite gbXML made up of Geometry from gbXML based on Mass families and Openings from gbXML based on Spaces.


Notes:
1. Depends on xgbxml developed by Dr. Steven Firth of Loughborough University.
2. xgbxml determines the destination surfaces of openings based on an adjustable distance tolerance.
3. Surfaces and openings shall be coplanar to ensure functionality.


Functional Development & Test:
Windows 10
Anaconda / Spyder IDE / Python 3.8
