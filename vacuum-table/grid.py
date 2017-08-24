#!python
#
# Generate grid for the vacuum table.
#

from dxfwrite import DXFEngine as dxf
import math
import sys

drawing = dxf.drawing('output-all-layers.dxf')

# All sizes in mm
board_w=2900
board_h=1600

# Air vent grid
spacing=20

# Diameter lucht gaatjes
diam_vent=4

# Diameter gaten voor bouten naar balken M6 of M8 slotbouten.
diam_support=8

# Pin for holding things M8
diam_peg = 12

# Support bars, across and per bar.
# Width is in mm; we assume a hole in the middle
support_bar=50	
support_n=8	
support_m=3

# Vent holes - 50 mm PC pipe
#
dia_vent=50
vents=[0,1,2,5]
# BBXes of the 4 vacuum area, in mm offset.
#
w1 = 600
w2 = 900
bbx=[
	[ spacing/4 + board_w / 2 - w1, spacing/4 + 150, w1, w1 * 0.7], # Approx A3
	[ spacing/4 + board_w / 2 - w2, spacing/4 + 150, w2, w2 * 0.7], # Approx A2
	[ spacing/4 + 0, spacing/4, board_w / 2, board_h ]
];

nw=int(math.floor(board_w/spacing))
nh=int(math.floor(board_h/spacing))

mx = nw * spacing
my = nh * spacing
ox = (board_w - mx) / 2
oy = (board_h - my) / 2

holes = [[0 for x in range(nh)] for y in range(nw)]
groves_h = [[0 for x in range(nh + 1)] for y in range(nw + 1)]
groves_v = [[0 for x in range(nh + 1)] for y in range(nw + 1)]

support_spacing_x=(board_w-support_bar) / ( support_n - 1 )
support_spacing_y=board_h / support_m
support_spacing_ox=support_bar / 2;
support_spacing_oy=support_spacing_y / (support_m -1 )

# Bolts for the support bars and extra mount points
#
for i in range(0,nw):
	for j in range(0,nh):
		x = ox + spacing * i
		y = oy + spacing * j

		# Remove the vent holes for the mounts to the supporting bars.
		#
		if (x - support_spacing_ox) % support_spacing_x < spacing:
			if  (y - support_spacing_oy)  % support_spacing_y < spacing:
				holes[i][j] = 1

		# Add an extra hole juist 'outside' the 4 corners of the inner 2 bbxen
		for k in range(0,2):
			b = bbx[k]
			i0 = int((b[0] - ox) / spacing)
			j0 = int((b[1] - oy) / spacing) 
			i1 = int((b[0] + b[2] - ox) / spacing) + 1
			j1 = int((b[1] + b[3] - oy) / spacing) + 1
			holes[i0][j0] = 2
			holes[i0][j1] = 2
			holes[i1][j0] = 2
			holes[i1][j1] = 2

		# Peg holes
		if  (i % 24 == 12 and j % 24 == 16):
				holes[i][j] = 2

		# if there is a hole - always remove the 4 groves around it.
		if holes[i][j]:
			groves_v[ i+0 ][ j+0] = 1
			groves_v[ i-1 ][ j+0] = 1
			groves_h[ i+0 ][ j+0] = 1
			groves_h[ i+0 ][ j-1] = 1

# Remove the groves around the various BBXes so they
# become separate areas
#
for b in bbx:
	x0 = b[0] - ox
	y0 = b[1] - oy
	x1 = x0 + b[2]
	y1 = y0 + b[3]
	i0 = int(x0 / spacing)
	i1 = int(x1 / spacing)
	j0 = int(y0 / spacing)
	j1 = int(y1 / spacing)
	for i in range(i0+1, i1 + 1):
		if (j0):
			groves_h[i][j0]=1
		groves_h[i][j1]= 1
	for j in range(j0+1, j1 + 1):
		if (i0):
			groves_v[i0][j]=1
		groves_v[i1][j]= 1

# vent holes in the middle of the smallest/first BBC
# and then in the middle of two support beams.
drawing.add_layer('suckholes', color=2)
for i in vents:
	b=bbx[1] 	# A2 box
	y = b[1] + b[3]/2
	x = support_spacing_ox + support_spacing_x /2 + i * support_spacing_x

	drawing.add(dxf.circle(dia_vent/2,(x,y), color=5))

drawing.add_layer('ventholes', color=2)
for i in range(0, nw):
	for j in range(0, nh):
		c = 3
		r = diam_vent/2

		# Assume this is a 'big' hole; rather than a normal vacuum hole.
		#
		if holes[i][j] == 1:
			r = diam_support
			c = 4
		if holes[i][j] == 2:
			r = diam_peg
			c = 2

		x = ox + i * spacing
		y = oy + j * spacing
		drawing.add(dxf.circle(r,(x,y), color=c))

# Various grooves. We try to figure out 'long' lines in one direction
# as opposed to drawing all the short CM pieces individually.
#
drawing.add_layer('groves', color=2)
for i in range(0, nw + 1):
	j = 0
	pen = 0
	while j < nh + 1:
		x = ox + i * spacing 
		y = oy + j * spacing
		if groves_h[i][j] or j >= nh:
			if pen:
				drawing.add(dxf.line((sx,sy),(x,y), color=7))
			pen = 0
		else:
			if not pen:
				sx = x
				sy = y
			pen = 1
		j = j + 1
	if pen:
		error
for j  in range(0, nh + 1):
	i = 0
	pen = 0
	while i < nw  + 1:
		x = ox + i * spacing
		y = oy + j * spacing
		if groves_v[i][j] or i >= nw:
			if pen:
				drawing.add(dxf.line((sx,sy),(x,y), color=7))
			pen = 0
		else:
			if not pen:
				sx = x
				sy = y
			pen = 1
		i = i + 1
	if pen:
		error

drawing.add_layer('annoations', color=2)

# Draw the outline of the board -- enlargen them by 1 mm so they do not clash with a CNC line
#
drawing.add(dxf.rectangle((0-1,-1),board_w+2, board_h+2, color = 1))

# draw each of the BBXes -- enlargen them by 1 mm so they do not clash with a CNC line
for b in bbx:
	drawing.add(dxf.rectangle((b[0]-1,b[1]-1),b[2]+2,b[3]+2, color = 3))

# drawing.add_layer('TEXTLAYER', color=2)
# drawing.add(dxf.text('Test', insert=(0, 0.2), layer='TEXTLAYER'))

drawing.save()
