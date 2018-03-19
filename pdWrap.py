from pandeia.engine.perform_calculation import perform_calculation
from pandeia.engine.instrument_factory import InstrumentFactory
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import yaml, json
import pdb
import os
import pandas
import glob
from astropy.io import ascii
from astropy.table import Table
import numpy as np
from joblib import Memory

memory = Memory(cachedir='cache')
pandeiaCalc = memory.cache(perform_calculation)

class pdWrap():
    """ A class that wraps Pandeia and lets me do my own scripts and calcs """
    def __init__(self,paramFile='yaml/grism_example.yaml'):
        """ pdWrap takes a parameter file to stick into Pandeia """
        self.pandeia_params = yaml.load(open(paramFile))
        self.prep_and_run()
        
    def prep_and_run(self):
        instrument = InstrumentFactory(self.pandeia_params['configuration'])
        ## Get the full well depth from the instrument parameters
        self.det_pars = instrument.get_detector_pars()
        self.fullWell = self.det_pars['fullwell']
        
        self.result = pandeiaCalc(self.pandeia_params)
    
    def get_well_depth_image(self):
        """ Get a well depth image """
        rampTime = self.result['information']['exposure_specification']['saturation_time']
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
        
    def plot_snr(self):
        """ Plots the signal to noise of a spectrum """
        fig, ax = plt.subplots()
        wave, snr = self.result['1d']['sn']
        ax.plot(wave,snr)
        ax.set_xlabel('Wavelength ($\mu$m)')
        ax.set_ylabel('SNR')
        fig.show()
    
    def max_well(self):
        """ Print the maximum well depth """
        maxVal = np.max(self.get_well_depth_image())
        return maxVal
        
    def relative_src_bg(self):
        """ Plots the relative source & Background """
        fig, ax = plt.subplots()
        
        for oneF in ['extracted_flux','extracted_bg_only']:
            wave, f = self.result['1d'][oneF]
            ax.plot(wave,f,label=oneF)
        ax.set_xlabel('Wavelength ($\mu$m)')
        ax.set_ylabel('Extracted Flux')
        ax.legend()
        
        fig.show()

def yaml_from_json(infile,outfile,simplifyBackg=True):
    """ Create an easier-to-read YAMl file from a JSON one
    Parameters
    ----------------
    infile: str
        Input JSON file
    outfile: str
        Output YAML file
    simplifyBackg: bool
        Simplify the background keyword?
    """
    ## Actually using YAML to load is cleaner
    inputDict = yaml.load(open(infile))
    
    if simplifyBackg == True:
        inputDict['background'] = 'medium'
    
    yaml.dump(inputDict,open(outfile,'w'),default_flow_style=False)

class pdFromDict(pdWrap):
    def __init__(self,paramDict):
        """ Create a Pandeia wrapper object from a dictionary rather than a YAML file """
        self.pandeia_params = paramDict
        self.prep_and_run()
        

def make_csvs():
    """ Make csv files (easier to version control) from excel"""
    for oneFile in glob.glob('excel/*.xlsx'):
        pd = pandas.read_excel(oneFile)
        outName = os.path.splitext(os.path.basename(oneFile))[0]
        pd.to_csv('lists/'+outName+'.csv',index=False)

def check_gto_wellFracs():
    """ Find the well fractions for GTO observations """
    inList = ascii.read('lists/gto_saturation_check.csv')
    pdGrism = yaml.load(open('yaml/grism_example.yaml'))
    
    outWell = []
    for oneObs in inList:
        pdGrism['scene'][0]['spectrum']['normalization']['norm_flux'] = float(oneObs['Kmag'])
        pdGrism['scene'][0]['spectrum']['normalization']['bandpass'] = str(oneObs['Norm Bandpass'])
        pdGrism['scene'][0]['spectrum']['sed']['teff'] = float(oneObs['Teff'])
        pdGrism['scene'][0]['spectrum']['sed']['log_g'] = float(oneObs['Logg'])
        pdGrism['scene'][0]['spectrum']['sed']['metallicity'] = float(oneObs['Metallicity'])
        pdGrism['configuration']['instrument']['filter'] = str(oneObs['Filter']).lower()
        pdGrism['configuration']['detector']['ngroup'] = int(oneObs['Ngroups'])
        pdGrism['configuration']['detector']['subarray'] = str(oneObs['Subarray']).lower()
        pdGrism['configuration']['detector']['readmode'] = str(oneObs['Read Mode']).lower()
        pd2 = pdFromDict(pdGrism)
        maxWell = np.max(pd2.get_well_depth_image())
        outWell.append(maxWell)
    inList['Well Frac'] = outWell
    inList.write('output/gto_wells.csv',overwrite=True)
