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
1. Depends on xgbxml (https://pypi.org/project/xgbxml/) developed by Dr. Steven Firth of Loughborough University.
2. Depends on topologicpy (https://test.pypi.org/project/topologicpy/) developed by Dr. Wassim Jabi of Cardiff University.
3. xgbxml: handling of gbxml elements like Surfaces and Openings.
4. topologicpy: determination of destination Surfaces of Openings with an adjustable Distance Tolerance.


Functional Development & Test:
  Windows 10 /
  Anaconda / Spyder IDE / Python 3.8 /
  xgbxml 0.0.8
  topologicpy 0.1.5
