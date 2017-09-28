#!python
#
# Generate grid for the vacuum table.
#

from dxfwrite import DXFEngine
import math
import sys

# Wether to use an actual point for a drill hole
# or a circle with a very small radius.
force_point = 1 
diam_point = 0.1 # mm

class DXFEngineExtras(DXFEngine):
    pass


    def bore(self,radius=1.0, center=(0., 0.), **kwargs):
        if force_point == 1:
            return self.point(center, **kwargs)
        if force_point:
            # Use the exact radius requested with 1% substracted and then 
            # rely on the tool setting in the mill machine on conjuction with 'bore' ?
            return self.circle(radius * 0.99, center, **kwargs)
        else:
            # ignore the radius given - rely on auto CNC spiral for small r.
            return self.circle(diam_point/2, center, **kwargs)

    def joinline(self, end=(0., 0.), start=(0., 0.), isFemale = True, **kwargs):
        x0, y0 = start
        x1, y1 = end

        ax = x1 - x0
        ay = y1 - y0
        l = math.sqrt(ax*ax+ay*ay)
        nj = int(l / spacing)

        px = board_d * ax / l / 2
        py = board_d * ay / l / 2

        extra = cutter_diameter / board_d

        if not isFemale:
             # move us in by the width of the board.
            x0 += py * 2
            x1 += py * 2
            y0 -= px * 2
            y1 -= px * 2
 
        out = []

        kwargs['layer'] = 'cut'
        cut= self.polyline(**kwargs)

        cut.add_vertex((x0,y0))
        for i in range(1,nj-1):
          p = (1 + 2 * i) / nj / 2
          x = x0 + p * ax
          y = y0 + p * ay

          if isFemale:
             cut.add_vertex((x-px,       y-py))
             cut.add_vertex((x-px+py,    y-py-px))
             cut.add_vertex((x-2*px+py,  y-2*py-px))
             cut.add_vertex((x-2*px+2*py,  y-2*py-2*px))
             cut.add_vertex((x-2*px+(2+extra)*py,  y-2*py-(2+extra)*px))
             cut.add_vertex((x-2*px+2*py,  y-2*py-2*px))
   
             cut.add_vertex((x+2*px+2*py,  y+2*py-2*px))
             cut.add_vertex((x+2*px+(2+extra)*py,  y+2*py-(2+extra)*px))
             cut.add_vertex((x+2*px+py,  y+2*py-px))
             cut.add_vertex((x+px+py,  y+py-px))
             cut.add_vertex((x+px, y+py))
          else:
             cut.add_vertex((x-2*px,     y-2*py))
             cut.add_vertex((x-2*px-2*py,y-2*py+2*px))
             cut.add_vertex((x+2*px-2*py,y+2*py+2*px))
             cut.add_vertex((x+2*px,     y+2*py))

             kwargs['layer'] = 'midway'
             midway1=self.polyline(**kwargs)
             midway1.add_vertices([
                (x-2*px+0*py,  y-2*py-0*px),
                (x-2*px-2*py,  y-2*py+2*px),
                (x-1*px-2*py,  y-1*py+2*px),
                (x-1*px+0*py,  y-1*py-0*px),
             ])
             # midway1.add_vertex((x-2*px+0*py,  y-2*py-0*px))
             midway1.close()
             out.append(midway1) 

             kwargs['layer'] = 'midway'
             midway2=self.polyline(**kwargs)

             midway2.add_vertices([
		(x+2*px+0*py,  y+2*py-0*px),
                (x+2*px-2*py,  y+2*py+2*px),
                (x+1*px-2*py,  y+1*py+2*px),
                (x+1*px+0*py,  y+1*py-0*px),
             ])
             # midway1.add_vertex((x-2*px+0*py,  y-2*py-0*px))
             midway2.close()
             out.append(midway2) 

        cut.add_vertex((x1,y1))

        if isFemale:
             return cut

        out.append(cut)
        return out
        

dxf = DXFEngineExtras()
drawing = dxf.drawing('output-all-layers.dxf')

drawing.add_layer('plate', color = 1)
drawing.add_layer('cut', color = 2)
drawing.add_layer('midway', color = 3)

# All sizes in mm
board_w=200
board_h=200
board_d=10
spacing=45
cutter_diameter = 6

drawing.add(dxf.rectangle((0,0), board_w,board_h, layer='plate'))

drawing.add(dxf.joinline((0,0),(board_w,0),False))
drawing.add(dxf.joinline((board_w,0),(board_w,board_h),True))
drawing.add(dxf.joinline((board_w,board_h),(0,board_h),True))
drawing.add(dxf.joinline((0,board_h),(0,0), False))

# drawing.add(dxf.circle(dia_vent/2,(x,y), color=5,layer='annotations'))
# drawing.add(dxf.bore(r,(x,y), color=c,layer='supports'))
# drawing.add(dxf.line((sx,sy),(x,y), color=7,layer='grooves'))

drawing.save()
