import os
import pickle
from openalea.plantgl.all import *

bgeom_dirpath = os.path.join("inputs", "scene0000.bgeom")
s = Scene(bgeom_dirpath)

Viewer.display(s)