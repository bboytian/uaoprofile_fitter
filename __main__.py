# imports
import sys

from .data_reader import main as data_reader
from .params import *


def main():
    datadir_l = sys.argv[1:]
    for data_dir in datadir_l:

        for ampmstr in [AMSTR, PMSTR]:
            # reading data
            df_l = data_reader(data_dir, ampmstr)

            # computing coefficients
            

            # printing coefficients
            print(coeff_a)

        print('\n')


if __name__ == '__main__':
    main()
