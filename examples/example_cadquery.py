import cadquery as cq
from ocp_vscode import *

rect_1 = cq.Workplane().rect(20,20)
rect_2 = rect_1.offset2d(-0.7)

show(rect_1, rect_2)