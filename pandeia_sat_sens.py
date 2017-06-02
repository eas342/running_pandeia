
# Import relevant libraries
## Following example from 
from pandeia.engine.perform_calculation import perform_calculation
import matplotlib.pyplot as plt
import yaml
import pdb

calc = yaml.load(open('yaml/default_nc_lw_imaging.yaml'))

result = perform_calculation(calc)

fig, ax = plt.subplots()

imMap = ax.imshow(result['2d']['saturation'])
ax.set_title('Saturation Map')
ax.set_xlabel('x')
ax.set_ylabel('y')
fig.colorbar(imMap)
fig.show()
pdb.set_trace()