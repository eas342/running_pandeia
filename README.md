# Example Pandeia Scripts

Some code to do exposure time calculations such as JWST saturation and sensitivity. Makes use of <a href="http://ssb.stsci.edu/pandeia/engine/1.0/">pandeia</a> scripts and runs `YAML` parameter files.

## Installing Pandeia
See <a href="https://pypi.python.org/pypi/pandeia.engine">https://pypi.python.org/pypi/pandeia.engine</a> for a few instructions. Check for the latest reference files there as well. To upgrade, run this:

	pip install pandeia.engine --upgrade

Edit your `.bash_profile` to reflect the latest reference data. For example:

	export pandeia_refdata="/jwst_stuff/pandeia_data-1.2"
with the path to the reference data.

## YAML FILES

Edit a file such as <a href="yaml/default_nc_lw_imaging.yaml">`yaml/default_nc_lw_imaging.yaml`</a>. Note that you can download the data from an ETC run online and use this as a start for future runs.

## Running
Simple run:

	python pandeia_sat_sens.py 


## Custom run

	import pdWrap
	pd = pdWrap.pdWrap('yaml/brown_dwarf_lrs.yaml')
	
# Plotting Results
There are some useful convenience functions for plotting results.

### Plot the well depth
Use the `pdWrap` object created by `pdWrap.pdWrap()`

	pd.plot_well_depth()

Also, you can simply get the maximum well depth with `pd.max_well()`.

### Plot the Signal to Noise

	pd.plot_snr()

### Plot the relative source & background within the aperture

	pdBD.relative_src_bg()

# Convenience Functions
This function makes a YAML file from the JSON, so it's a little easier to read. Also, for easier reading, it replaces the manual background with 'medium'.

	pdWrap.yaml_from_json('json/bd_wd_online.json','yaml/new_yaml.yaml')	
	

# Notes on Pandeia's Python API

## Exposure Specification

There doesn't seem to be a special parameter for the number of amplifier output channels. Rather, there are different subarray names:

 - `full`
 - `subgrism256 (noutputs=1)`
 - `subgrism256`
 - `subgrism128`
 - `subgrism128 (noutputs=1)`
 - `subgrism64`
 - `subgrism64 (noutputs=1)`

## Exposure Specification
Some useful info on the results can be printed with 

	pd1 = pdWrap.pdWrap()
	pd1.result['information']

One can examine the instrument parameters by running Pandeia's instrument factory:

	pd1 = pdWrap.pdWrap()
	inst = pdWrap.InstrumentFactory(pd1.pandeia_params['configuration'])
	inst.subarray_config
	
The last command will show the available subarrays. One can check the exposure and frame times with.

	exp1 = inst.get_exposure_pars()
	exp1.tframe

## Saturation
The saturation map is viewable from Pandeia wiht

	result = peform_calculation(parameters)
	np.max(result['2d']['saturation'])
