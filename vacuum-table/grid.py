#!python
#
# Generate grid for the vacuum table.
#

from dxfwrite import DXFEngine as dxf
import math
import sys

drawing = dxf.drawing('output-all-layers.dxf')		# Everything
grooves = dxf.drawing('output-grooves-layer.dxf')		# groeven plaat 2
supports = dxf.drawing('output-suports-layer.dxf')		# plaat 3 - diep 8mm gat, ook door de alu balk,
slotkop = dxf.drawing('output-slotkop-layer.dxf')		# plaat 2  (of onderkant 3) - slotbout koppen
pegs = dxf.drawing('output-pegs-layer.dxf')		# alle platen (door en door)
vents = dxf.drawing('output-vents-layer.dxf')		# plaat 3,4,5

point = 1

# All sizes in mm
board_w=2560	# 2559.42 is actual max (from -3.0)
board_h=1510	# 1509.121

# Air vent grid
spacing=20

# Diameter lucht gaatjes
diam_vent=4

# Diameter gaten voor bouten naar balken M6 of M8 slotbouten.
diam_support=8
diam_slotkop=20.7	# DIN 603
# Pin for holding things M8
diam_peg = 12

# Support bars, across and per bar.
# Width is in mm; we assume a hole in the middle
support_bar=40	# width of the bar in MM
support_n=15	# number of bars; including the end one
support_m=3
support_ox=2.6
# Rather than calculate this - use the size Rene measured; checked at bar 14
support_spacing_x=190
#
# support_spacing_x=(board_w-support_bar) / ( support_n - 1 )
# Vent holes - 50 mm PC pipe
#
dia_vent=50
suckers=[0,1,2,5]

# A0	841 x 1189 mm
# A1	594 x 841 mm
# A2	420 x 594 mm
# A3	297 x 420 mm
# A4	210 x 297 mm	
A2w=594
A2h=420

A3w=420
A3h=297

A4w=297
A4h=210

gamma_w = 2440
gamma_h = 1220

off = (board_h - gamma_h)/2
offx = 10

bbx=[
	# [ spacing/4 + board_w / 2 - A4w, spacing/4 + 150, A4w, A4h], # Approx A4
	[ offx + spacing/4 + board_w / 2 - A3w, spacing/4 + off, A3w, A3h], # Approx A3
	# [ spacing/4 + board_w / 2 - w2, spacing/4 + off, w2, w2 * 0.7], 
	# [ spacing/4 + 0, spacing/4 + off, board_w / 2, board_h / 2], # Approx quarter board
	# [ spacing/4 + 0, spacing/4, board_w / 2, board_h ]		# half board
	# Een kleine vacuumsectie richting A2 lijkt mij nuttig, evenals een gebied voor een kwart plaat (72,5x125) en een gehele (125 * 250).  
	[ offx + spacing/4 + board_w / 2 - gamma_w / 2, spacing/4 + off, gamma_w /2 , gamma_h / 2 ],	# kwart gamma plaat
	[ offx + spacing/4 + board_w / 2 - gamma_h, spacing/4 + off, gamma_h, gamma_w / 2 ],		# halve gamma plaat
	[ offx +  spacing/4 + board_w / 2 - gamma_h, spacing/4 + off, gamma_w, gamma_h ],		# hele gamma plaat
];

nw=int(math.floor(board_w/spacing))
nh=int(math.floor(board_h/spacing))

mx = nw * spacing
my = nh * spacing
# ox = (board_w - mx) / 2
ox = support_ox + support_bar / 2

oy = (board_h - my) / 2

holes = [[0 for x in range(nh+3)] for y in range(nw+3)]
groves_h = [[0 for x in range(nh + 1)] for y in range(nw + 1)]
groves_v = [[0 for x in range(nh + 1)] for y in range(nw + 1)]

support_spacing_y=board_h / support_m
support_spacing_ox=support_ox + support_bar / 2;
support_spacing_oy=support_spacing_y / (support_m -1 )

# Bolts for the support bars and extra mount points
#
for i in range(0,nw+1):
	for j in range(0,nh):
		x = ox + spacing * i
		y = oy + spacing * j

		# Wipe the whole outside area
		#
		outside = bbx[3]
		if x < outside[0] or x > outside[0] + outside[2] or y < outside[1] or y > outside[1] + outside[3]:
			holes[i][j] = -1

		# Remove the vent holes for the mounts to the supporting bars.
		# Do this every other bar - as our bars are in a 190 grid which
		# is not a clean multiple of the 20 grid of the vents.
		#
		if (x - support_spacing_ox) % (2 * support_spacing_x) < spacing:
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
		#
		if  i % 19 == 12 and j % 24 == 16:
				holes[i][j] = 2
		# extra on eithe end
		# if  ((i == 12) or (i==145)) and j % 12 == 8:
		#		holes[i][j] = 2


		# if there is a hole - always remove the 4 groves around it.
		if holes[i][j]:
			groves_v[ i+0 ][ j+0] = 1
			groves_v[ i-1 ][ j+0] = 1
			groves_h[ i+0 ][ j+0] = 1
			groves_h[ i+0 ][ j-1] = 1

# 2 peag holes far left/right on 1/3rd
holes[ 2 ][ nh / 2 - 10] = 2
holes[ nw - 2 ][ nh / 2 - 10] = 2
holes[ 2 ][ nh / 2 + 10] = 2
holes[ nw - 2 ][ nh / 2 + 10] = 2

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
for i in suckers:
	b=bbx[1] 	# A2 box
	y = b[1] + b[3]/2
	x = support_spacing_ox + support_spacing_x /2 + i * support_spacing_x

	drawing.add(dxf.circle(dia_vent/2,(x,y), color=5))

drawing.add_layer('ventholes', color=2)
for i in range(0, nw): # +1
	for j in range(0, nh): # +1
		c = 3
		r = diam_vent/2

		if holes[i][j] < 0:
			continue

		x = ox + i * spacing
		y = oy + j * spacing

		# Assume this is a 'big' hole; rather than a normal vacuum hole.
		#
		if holes[i][j] == 1:
			r = diam_support
			c = 4
			drawing.add(dxf.circle(r,(x,y), color=c))
			if point:
				supports.add(dxf.circle(point,(x,y),color=7))
			else:
				supports.add(dxf.point((x,y),color=7))
			slotkop.add(dxf.circle(diam_slotkop,(x,y), color=c))
		else: 
 		  if holes[i][j] == 2:
			r = diam_peg
			c = 2
			drawing.add(dxf.circle(r,(x,y), color=c))
			if point:
				pegs.add(dxf.circle(point,(x,y),color=7))
			else:
				pegs.add(dxf.point((x,y),color=7))
		  else:
			drawing.add(dxf.circle(r,(x,y), color=c))
			if point:
				vents.add(dxf.circle(point,(x,y),color=7))
			else:
				vents.add(dxf.point((x,y),color=7))

# odd bar mounting holes - outside the suction area to not clash with the grid
for i in range(1,support_n,2):
	x = ox + support_spacing_x * i
	r = diam_support
	c= 4
	y = bbx[3][1] - 30
	drawing.add(dxf.circle(r,(x,y), color=c))
	if point:
		supports.add(dxf.circle(point,(x,y),color=7))
	else:
		supports.add(dxf.point((x,y),color=7))
	slotkop.add(dxf.circle(diam_slotkop,(x,y), color=c))

	y = bbx[3][1] +bbx[3][3] + 30
	drawing.add(dxf.circle(r,(x,y), color=c))
	if point:
		supports.add(dxf.circle(point,(x,y),color=7))
	else:
		supports.add(dxf.point((x,y),color=7))
	slotkop.add(dxf.circle(diam_slotkop,(x,y), color=c))



# Various grooves. We try to figure out 'long' lines in one direction
# as opposed to drawing all the short CM pieces individually.
#
drawing.add_layer('groves', color=2)
for i in range(0, nw):
	j = 0
	pen = 0
	while j < nh + 1:
		x = ox + i * spacing 
		y = oy + j * spacing
		if groves_h[i][j] or j >= nh:
			if pen:
				drawing.add(dxf.line((sx,sy),(x,y), color=7))
				grooves.add(dxf.line((sx,sy),(x,y), color=7))
			pen = 0
		else:
			if not pen:
				sx = x
				sy = y
			pen = 1
		j = j + 1
	if pen:
		error
for j  in range(0, nh):
	i = 0
	pen = 0
	while i < nw  + 1:
		x = ox + i * spacing
		y = oy + j * spacing
		if groves_v[i][j] or i >= nw:
			if pen:
				drawing.add(dxf.line((sx,sy),(x,y), color=7))
				grooves.add(dxf.line((sx,sy),(x,y), color=7))
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

# Draw each support bart - with a center lines to check the support slotbouten.
#
for i in range(0,support_n):
	x = support_ox + support_spacing_x * i
	drawing.add(dxf.rectangle((x, -20), support_bar, board_h + 40, color = 1))
	drawing.add(dxf.line((x + support_bar /2, -10), (x + support_bar /2, board_h + 20), color = 1))

# draw each of the BBXes -- enlargen them by 1 mm so they do not clash with a CNC line
for b in bbx:
	drawing.add(dxf.rectangle((b[0]-1,b[1]-1),b[2]+2,b[3]+2, color = 3))

# drawing.add_layer('TEXTLAYER', color=2)
# drawing.add(dxf.text('Test', insert=(0, 0.2), layer='TEXTLAYER'))

drawing.save()
grooves.save()
supports.save()
slotkop.save()
vents.save()
pegs.save()
