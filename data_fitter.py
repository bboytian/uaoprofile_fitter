# imports
from itertools import combinations, permutations

import numpy as np
import scipy.interpolate as spip

from .params import *


# main func
def main(df_l):
    '''
    Interpolates all points provided by the dataframe.
    Goes through every possible pair combination specified in .params.COMPARELST

    ADD IN A BOOLEAN FEATURE TO

    Parameters
        df_l (list): list of pandas.Dataframes, each df corresponding to a
                     measurement

    Returns
        compcol_tl (list): list of comparison column pair tuples
        aVSbcoeff_al (list): list of coefficients for polynomial fit, in the
                             same order as compcol_tl. a is x-array, b is y-array
        bVSacoeff_al (list): like above but reversed
    '''
    compcol_tl = list(combinations(COMPARELST, 2))

    aVSbcoeff_al, bVSacoeff_al = [], []
    for compcol_t in compcol_tl:
        a_al, b_al = [], []
        for df in df_l:
            a_al.append(df[COLDIC[compcol_t[0]]])
            b_al.append(df[COLDIC[compcol_t[1]]])
        a_a, b_a = np.concatenate(a_al, axis=0), np.concatenate(b_al, axis=0)

        orderind = b_a.argsort()
        b_a = b_a[orderind]
        a_a = a_a[orderind]

        # orderind = a_a.argsort()
        # b_a = b_a[orderind]
        # a_a = a_a[orderind]   
        

        boo_a = (b_a < 287) * (b_a >200)
        b_a = b_a[boo_a]
        a_a = a_a[boo_a]

        print(b_a)

        # aVSbcoeff_a = np.polyfit(a_a, np.log(b_a), POLYDEG)[::-1]
        # bVSacoeff_a = np.polyfit(b_a, a_a, POLYDEG)[::-1]

        # aVSbcoeff_a = spip.interp1d(a_a, b_a, kind='quadratic', fill_value='extrapolate')
        bVSacoeff_a = spip.interp1d(b_a, a_a, kind='quadratic', fill_value='extrapolate')

        # aVSbcoeff_al.append(aVSbcoeff_a)
        bVSacoeff_al.append(bVSacoeff_a)



    import matplotlib.pyplot as plt

    tb_a = np.linspace(b_a.min(), b_a.max(), 10000)
    # ta_a = np.sum(
    #     [(tb_a**i)*bVSacoeff for i, bVSacoeff in enumerate(bVSacoeff_al[0])],
    #     axis=0
    # )
    ta_a = bVSacoeff_al[0](tb_a)
    plt.figure(str(compcol_t))
    print(f'plotting x:{compcol_t[1]}, y:{compcol_t[0]}')
    plt.plot(b_a, a_a, 'ko')
    plt.plot(tb_a, ta_a)

    # ta_a = np.linspace(a_a.min(), a_a.max(), 10000)
    # # tb_a = np.exp(np.sum(
    # #     [(ta_a**i)*aVSbcoeff for i, aVSbcoeff in enumerate(aVSbcoeff_al[0])],
    # #     axis=0
    # # ))
    # tb_a = bVSacoeff_al[0](ta_a)    
    # plt.figure(str(compcol_t))
    # print(f'plotting x:{compcol_t[1]}, y:{compcol_t[0]}')
    # plt.plot(a_a, b_a, 'ko')
    # plt.plot(ta_a, tb_a)

    plt.show()



    return compcol_tl, aVSbcoeff_al, bVSacoeff_al





# testing
if __name__ == '__main__':

    # imports
    import matplotlib.pyplot as plt
    from .data_reader import main as data_reader

    # params
    data_dir = '/home/tianli/SOLAR_EMA_project/data/UAO_profiles/UAO_raw_data_2019/201905'
    ampmstr = '0000'
    df_l = data_reader(data_dir, ampmstr)

    compcol_tl, aVSbcoeff_al, bVSacoeff_al = main(df_l)

    # for i, compcol_t in enumerate(compcol_tl):

    #     a_al, b_al = [], []
    #     for df in df_l:
    #         a_al.append(df[COLDIC[compcol_t[0]]])
    #         b_al.append(df[COLDIC[compcol_t[1]]])
    #     a_a, b_a = np.concatenate(a_al, axis=0), np.concatenate(b_al, axis=0)

    #     # b_a = np.log(b_a)

    #     tb_a = np.linspace(b_a.min(), b_a.max(), 10000)
    #     ta_a = np.sum(
    #         [(tb_a**j)*bVSacoeff for j, bVSacoeff in enumerate(bVSacoeff_al[i])]
    #         , axis=0
    #     )


    #     ta_a = np.linspace(a_a.min(), a_a.max(), 10000)
    #     tb_a = np.sum(
    #         [(ta_a**j)*aVSbcoeff for j, aVSbcoeff in enumerate(aVSbcoeff_al[i])]
    #         , axis=0
    #     )

    #     plt.figure(str(compcol_t))
    #     print(f'plotting x:{compcol_t[1]}, y:{compcol_t[0]}')
    #     plt.plot(b_a, a_a, 'ko')
    #     plt.plot(tb_a, ta_a)


    # plt.show()
