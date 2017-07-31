
# Import relevant libraries
## Following example from 
from pandeia.engine.perform_calculation import perform_calculation
from pandeia.engine.instrument_factory import InstrumentFactory
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import yaml
import pdb

params = yaml.load(open('yaml/grism_example.yaml'))

## Get the full well depth from the instrument parameters
instrument = InstrumentFactory(params['configuration'])
det_pars = instrument.get_detector_pars()
fullWell = det_pars['fullwell']

result = perform_calculation(params)

## Gets the well fraction
wellFrac = result['information']['exposure_specification']['tsat'] * result['2d']['detector'] / det_pars['fullwell']

fig, ax = plt.subplots()

imMap = ax.imshow(wellFrac)
ax.set_title('Well Fraction Map Map')
ax.set_xlabel('x')
ax.set_ylabel('y')

## Adjust colorbar height to match image
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.05)
fig.colorbar(imMap,label='Well Fraction',cax=cax)
fig.show()
pdb.set_trace()
