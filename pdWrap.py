from pandeia.engine.perform_calculation import perform_calculation
from pandeia.engine.instrument_factory import InstrumentFactory
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import yaml
import pdb
import os
import pandas
import glob

class pdWrap():
    """ A class that wraps Pandeia and lets me do my own scripts and calcs """
    def __init__(self,paramFile='yaml/grism_example.yaml'):
        """ pdWrap takes a parameter file to stick into Pandeia """
        self.pandeia_params = yaml.load(open(paramFile))
        
        instrument = InstrumentFactory(self.pandeia_params['configuration'])
        ## Get the full well depth from the instrument parameters
        self.det_pars = instrument.get_detector_pars()
        self.fullWell = self.det_pars['fullwell']
        
        self.result = perform_calculation(self.pandeia_params)
    
    def get_well_depth_image(self):
        """ Get a well depth image """
        rampTime = self.result['information']['exposure_specification']['tramp']
        wellFrac = rampTime * self.result['2d']['detector'] / self.fullWell
        
        return wellFrac
        
    def plot_well_depth(self):
        """ Plots the well depth as an image """
        fig, ax = plt.subplots()
        imMap = ax.imshow(self.get_well_depth_image())
        ax.set_title('Well Fraction Map Map')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        
        ## Adjust colorbar height to match image
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        fig.colorbar(imMap,label='Well Fraction',cax=cax)
        fig.show()


def make_csvs():
    """ Make csv files (easier to version control) from excel"""
    for oneFile in glob.glob('excel/*.xslx'):
        pd = pandas.read_excel(oneFile)
        outName = os.path.splitext(os.path.basename(oneFile))[0]
        pd.to_csv('lists/'+outName+'.csv',index=False)

def check_gto_wellFracs():
    """ Find the well fractions for GTO observations """
    