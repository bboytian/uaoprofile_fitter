# imports
from itertools import combinations, permutations

import numpy as np

from ..params import *


# params

_aname = 'P'
_bname = 'Altitude'


# main func
def main(df_l):
    '''
    Interpolates all points provided by the dataframe.

    ADD IN A BOOLEAN FEATURE TO

    Parameters
        df_l (list): list of pandas.Dataframes, each df corresponding to a
                     measurement

    Returns
         coeff_l (list): list of coeffcients
         descrip_l (list): list of string descriptions for each coeff list
    '''
    a_al, b_al = [], []
    for df in df_l:
        a_al.append(df[COLDIC[_aname]])
        b_al.append(df[COLDIC[_bname]])
    a_a, b_a = np.concatenate(a_al, axis=0), np.concatenate(b_al, axis=0)

    aVSbcoeff_a = np.polyfit(a_a, np.log(b_a), POLYDEG)[::-1]
    aVSbdescrip = f'x: {_aname}, y: ln({_bname})'

    bVSacoeff_a = np.polyfit(b_a, a_a, POLYDEG)[::-1]
    bVSadescrip = f'x: {_bname}, y: {_aname}'

    return [aVSbcoeff_a, bVSacoeff_a], [aVSbdescrip, bVSadescrip]





# testing
if __name__ == '__main__':
    '''
    This script is written to check that the interpolation is done well
    '''

    # imports
    from glob import glob
    import matplotlib.pyplot as plt
    from ..data_reader import main as data_reader

    # params
    data_dir = glob(REGEXDIR)[0]  # regex directory containing multiple dates
    ampmstr = AMSTR

    df_l = data_reader(data_dir, ampmstr)

    [aVSbcoeff_a, bVSacoeff_a], [aVSbdescrip, bVSadescrip] = main(df_l)

    a_al, b_al = [], []
    for df in df_l:
        a_al.append(df[COLDIC[_aname]])
        b_al.append(df[COLDIC[_bname]])
    a_a, b_a = np.concatenate(a_al, axis=0), np.concatenate(b_al, axis=0)
    plt.plot(b_a, a_a, 'ko', alpha=0.1)


    tb_a = np.linspace(b_a.min(), b_a.max(), 10000)
    ta_a = np.sum(
        [(tb_a**j)*bVSacoeff for j, bVSacoeff in enumerate(bVSacoeff_a)],
        axis=0
    )
    plt.plot(tb_a, ta_a, label=bVSadescrip)


    ta_a = np.linspace(a_a.min(), a_a.max(), 10000)
    tb_a = np.exp(np.sum(
        [(ta_a**j)*aVSbcoeff for j, aVSbcoeff in enumerate(aVSbcoeff_a)],
        axis=0
    ))

    plt.plot(tb_a, ta_a, label=aVSbdescrip)

    plt.legend()
    plt.show()
