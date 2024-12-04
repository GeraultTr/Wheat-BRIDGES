import os
import pickle
from openalea.plantgl.all import *

bgeom_dirpath = os.path.join("inputs", "scene0000.bgeom")
s = Scene(bgeom_dirpath)

# mtg_filename = "0"
# mtg_dirpath = os.path.join("outputs", f"{mtg_filename}.pckl")

# with open(mtg_dirpath, "rb") as f:
#     g = pickle.load(f)



# # We initialize a turtle in PlantGL:
# turtle = turt.PglTurtle()
# # We make the graph upside down:
# turtle.down(180)
# # We initialize the scene with the MTG g:
# scene = turt.TurtleFrame(g, turtle=turtle, gc=False)

Viewer.display(s)