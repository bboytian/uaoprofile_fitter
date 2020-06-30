# imports
from glob import glob
import os.path as osp

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# params
datastr = '????????{}P???????_UPP_EDT_48698.txt'  # format am or pm string
ampmstr = '1200'                                  # am->'0000', pm->'1200'
ampmstr = '0000'                                  # am->'0000', pm->'1200'

col_d = {
    'time': 'Time [sec]',
    'P': 'P [mB]',
    'T': 'T [�C]',
    'U': 'U [%]',
    'Wsp': 'Wsp [kn]',
    'Wdir': 'Wdir',
    'Altitude': 'Altitude',
    'GeoPot': 'GeoPot',
    'DewPoint': 'DewPoint',
    'Rs': 'Rs [m/s]',
    'D': 'D [kg/m3]',
    'Azimuth': 'Azimuth',
    'Elevation': 'Elevation',
    'Range': 'Range',
}
headerind = 1
endstr = 'Tropopauses:'

dtaltlow, dtalthigh = 0, 60     # conservative gradient thres


# main func
def main(datadir, pltcolor):

    # reading data
    dir_l = glob(osp.join(data_dir, datastr.format(ampmstr)))

    df_l = []
    for file_dir in dir_l:

        # reading from text file
        df = pd.read_fwf(file_dir, header=headerind)
        # trimming off meta at the end
        endind = np.argmax(df[col_d['time']] == endstr)
        if not endind:
            endind = None
        df = df[:endind]
        # popping badly formatted columns
        df = df[df.columns[df.columns.isin(list(col_d.values()))]]
        # replace '-' in data
        df = df.replace({'-': None})
        # changing data type
        df = df.astype('float64')

        # cleaning up;thresholding by altitude vs time gradient
        ## computing gradient
        dtalt_a = np.gradient(df[col_d['Altitude']], df[col_d['time']])
        dtaltboo_a = (dtalt_a > dtaltlow) * (dtalt_a < dtalthigh)
        
        df_l.append(df)

    # Plotting
    for df in df_l:
        # plt.plot(df[col_d['P']].values, df[col_d['Altitude']].values,
        #          color=pltcolor)
        # plt.plot(df[col_d['time']].values, df[col_d['Altitude']].values)
        pass




# running
if __name__ == '__main__':

    for i, data_dir in enumerate(glob(
            '/home/tianli/SOLAR_EMA_project/data/UAO_profiles/UAO_raw_data_2019/2019*'
    )):
        main(data_dir, f'C{i}')

    # plt.yscale('log')
    plt.show()
