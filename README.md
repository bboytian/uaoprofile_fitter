# uaoprofile_fitter

## Usage

Utilse a conda environment provided by `.environment.yml`. To install the environment, run:
```
conda env create -n <name of environment> /path/to/uaoprofile_fitter/environment.yml
```

From outside the package directory, run:
```
python -m uaoprofile_fitter <datadir1> [<datadir2> [...]]
```

Output will be the fitted coefficients for all the data points within the month.
Two sets of coefficients are printed, the first is for 'am, and the second for 'pm'.
Coefficients are in ascending polynomial power.
Coefficients sets between data directories are seperated by a newline 


## Configuration

All configurable qualities of the code can be adjusted in `.params`

## Future Development

Data fitters library can be expanded, and called in `__main__` by specifying the right fitter in .params