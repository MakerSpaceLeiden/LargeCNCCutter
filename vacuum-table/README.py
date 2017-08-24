Generates the vacuum table DXF files.

Requires
	Python 2.7
	dxfwrite (1.2.1)  - A Python library to create DXF R12 drawings.

Yoy may also want to use:
	Cnc25D (0.1.10)   - CAD library for 2.5D parts (including gears) using svgwrite, dxfwrite or FreeCAD as backend

Usage:
	python grid.py

The result is a file called

	output-all-layers.dxf

which can be loaded onto the CNC machine. Note that it contains multiple layers; with different router bit requirements/expectations and to be cut into 3 different sheets of plywood or MDF
