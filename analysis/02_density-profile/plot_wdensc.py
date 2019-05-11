
# /dfs2/tw/limvt/08_permeate/github/analysis/02_density-profile/plot_wdensc.py

import numpy as np
import matplotlib.pyplot as plt
import re

def plot_profile(files, binvol):

    fig1, ax1 = plt.subplots()
    fig2, ax2 = plt.subplots()

    for fname in files:
        x, y = np.loadtxt(fname, usecols=(0, 1), unpack=True)
        l = re.split('[_.]', fname)[2]

        if l == 'water':
            atoms = 3
        elif l == 'lipid':
            atoms = 134  # 52 heavy atoms, 134 total atoms
        elif l == 'tails':
            atoms = 96
        elif l == 'carbonyl':
            atoms = 6
        elif l == 'glycerol':
            atoms = 8
        elif l == 'phosphate':
            atoms = 5
        elif l == 'choline':
            atoms = 19

        ax1.plot(x, y, label=l)
        ax2.plot(x, y/binvol/atoms, label=l)

    ax1.legend(loc=(1.04, 0.5))
    ax2.legend(loc=(1.04, 0.5))
    fig1.savefig('plot_raw.png', bbox_inches = 'tight')
    fig2.savefig('plot_scaled.png', bbox_inches = 'tight')
    plt.show()

if __name__ == "__main__":

    import argparse
    import matplotlib.pyplot as plt
    parser = argparse.ArgumentParser()

    parser.add_argument("-f", "--files", required=True, nargs='+',
                        help="One or more files to be processed")

    parser.add_argument("-b", "--binvol", type=float,
                        help="Bin volume to divide data by. wdensC prints this in header")

    parser.add_argument("-p", "--pka", action="store_true", default=False,
                        help="Compute pKa shift profile from neutral PMF in -0"
                        " flag and charged PMF in -1 flag")

    args = parser.parse_args()
    plot_profile(args.files, args.binvol)

