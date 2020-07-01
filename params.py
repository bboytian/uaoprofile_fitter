# data reading params
REGEXDIR = '/home/tianli/Santo_Shared_Projects/From_Tianli/UAO_profiles/UAO_raw_data_2019/*'
DATAFILE = '????????{}P???????_UPP_EDT_48698.txt'  # format am or pm string
PMSTR = '1200'                                  # am->'0000', pm->'1200'
AMSTR = '0000'                                  # am->'0000', pm->'1200'

COLDIC = {
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

UNITSCALEDIC = {
    'Altitude': 0.0003048       # feet to km
}

HEADERIND = 1
ENDSTR = 'Tropopauses:'


# data cleaning params
DTALTLOW, DTALTHIGH = 15*0.0003048, 60*0.0003048  # conservative gradient thres
WINDOWSIZE = 7                                    # odd number


#  data fitting params
FITTER = 'PvsAltitdue'          # choose from .data_fitters
POLYDEG = 6
