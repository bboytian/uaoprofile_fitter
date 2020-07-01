# imports
from glob import glob
import sys

import numpy as np

from .data_reader import main as data_reader
from .params import *


# main func
def main():
    # print settings
    np.set_printoptions(linewidth=np.inf)

    # retriving data file directories
    if len(sys.argv) > 1:
        datadir_l = sys.argv[1:]
    else:
        datadir_l = glob(REGEXDIR)
    datadir_l.sort()

    for data_dir in datadir_l:
        # print(f'working on: {data_dir}')

        for ampmstr in [AMSTR]:#, PMSTR]:
            # print(f'coeff for {ampmstr}hrs')
            # reading data
            df_l = data_reader(data_dir, ampmstr)

            # computing coefficients
            exec(f'from .data_fitters import {FITTER} as data_fitter', globals())
            coeff_l, descrip_l = data_fitter(df_l)

            # printing coefficients
            for i, descrip in enumerate(descrip_l):
                if i != 1:
                    continue
                # print(descrip)
                print(coeff_l[i])
            # print('\n')

        # print('\n\n')


if __name__ == '__main__':
    main()
