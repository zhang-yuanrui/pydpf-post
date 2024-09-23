import sys

sys.path.insert(0, r'C:\Users\yuzhang\dpf-post\src')

from ansys.dpf import post
from ansys.dpf.post import examples

simulation = post.load_simulation(examples.download_crankshaft())

# plot = simulation.plot()

displacement = simulation.displacement()
displacement.plot(screenshot="./crankshaft_disp.png")