# Example Pandeia Scripts

Some code to do exposure time calculations such as JWST saturation and sensitivity. Makes use of <a href="http://ssb.stsci.edu/pandeia/engine/1.0/">pandeia</a> scripts and runs `YAML` parameter files.

## YAML FILES

Edit a file such as <a href="yaml/default_nc_lw_imaging.yaml">`yaml/default_nc_lw_imaging.yaml`</a>

## Running

	python pandeia_sat_sens.py 


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
