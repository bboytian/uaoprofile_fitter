# imports
from glob import glob
import os.path as osp

import numpy as np
import pandas as pd

from .params import *


# main func
def main(datadir, ampmstr):
    '''
    Parameters
        datadir (str): absolute directory containing datafiles
        ampmstr (str): determines 'am' or 'pm' data
                       'am' -> '0000'
                       'pm' -> '1200'
    Return
        df_l (list): list of dataframes, each dataframe representing a
                     measurement within the provided directory
    '''

    # reading data
    dir_l = glob(osp.join(datadir, DATAFILE.format(ampmstr)))

    df_l = []
    for file_dir in dir_l:

        # reading from text file
        df = pd.read_fwf(file_dir, header=HEADERIND)
        # trimming off meta at the end
        endind = np.argmax(df[COLDIC['time']] == ENDSTR)
        if not endind:
            endind = None
        df = df[:endind]
        # popping badly formatted columns
        df = df[df.columns[df.columns.isin(list(COLDIC.values()))]]
        # replace '-' in data
        df = df.replace({'-': None})
        # changing data type
        df = df.astype('float64')
        # scaling units
        for key in UNITSCALEDIC:
            df[COLDIC[key]] = df[COLDIC[key]] * UNITSCALEDIC[key]

        # cleaning up;thresholding by altitude vs time gradient
        dtalt_a = np.gradient(df[COLDIC['Altitude']], df[COLDIC['time']])
        ## gradient threshold boolean
        dtaltboo_a = (dtalt_a > DTALTLOW) * (dtalt_a < DTALTHIGH)
        ## moving window boolean
        dtaltboo_a = np.convolve(
            dtaltboo_a, np.ones(WINDOWSIZE, dtype=np.int),
            'same'
        ) >= int(WINDOWSIZE/2) + 1
        ## applying boolean
        df = df[dtaltboo_a]

        df_l.append(df)

    return df_l


# testing
if __name__ == '__main__':
    '''
    This script is written to check that the data cleaning parameters are
    working well for the given dataset.
    configure regexdir to be able to see whatever dataset you want to see
    each color represents one data directory in the regex directory
    '''
    # imports
    import matplotlib.pyplot as plt

    # params
    regexdir = REGEXDIR  # regex directory containing multiple dates
    ampmstr = AMSTR

    # running
    for i, data_dir in enumerate(glob(regexdir)):

        if data_dir != osp.join(REGEXDIR[:-1], '201905'):
            continue
        
        print(f'working on {data_dir}')
        df_l = main(data_dir, ampmstr)

        # Plotting
        for df in df_l:
            pltcolor = f'C{i}'

            # plot altitiude against pressure
            # plt.plot(df[COLDIC['P']].values, df[COLDIC['Altitude']].values,
            #          color=pltcolor)

            # plot altitude against time
            plt.plot(df[COLDIC['time']].values, df[COLDIC['Altitude']].values,
                     color=pltcolor)

            
    plt.show()
