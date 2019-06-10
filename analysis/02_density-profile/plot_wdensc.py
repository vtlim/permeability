
# Location: /dfs2/tw/limvt/08_permeate/github/analysis/02_density-profile/plot_wdensc.py

import numpy as np
import matplotlib.pyplot as plt
import re

from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle

def draw_window_boxes(ax, xdata, ydata, widths, colors, alpha=0.5):
    # adapted from: https://matplotlib.org/gallery/statistics/errorbars_and_boxes.html

    # Create list for all the error patches
    errorboxes = []

    # Loop over data points; create box from errors at each point
    for x, y, w, c in zip(xdata, ydata, widths, colors):
        rect = Rectangle((x, y), w, 0.001, color=c, alpha=alpha, edgecolor='None')
        ax.add_patch(rect)


def plot_profile(files, binvol, scale_component=False):
    # scale by component to get density by number of mols instead of number of atoms

    fig1, ax1 = plt.subplots()
    if scale_component:
        fig2, ax2 = plt.subplots()

    for fname in files:
        x, y = np.loadtxt(fname, usecols=(0, 2), unpack=True)
        l = re.split('[_.]', fname)[2]

        if scale_component:
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
            ax2.plot(x, y/binvol/atoms, label=l)

        ax1.plot(x, y, label=l)

    # draw boxes of window definitions
    boxes_x = np.array([-40, -34, -26, -20, -12, -6, 2, 8, 16, 22, 30])
    boxes_y = np.array([-0.002, -0.003]*5 + [-0.002])
    widths = np.array([10,12]*5 + [10])
    colors = ['blue','red']*5+['blue']
    _ = draw_window_boxes(ax1, boxes_x, boxes_y, widths, colors)

    ax1.legend(loc=(1.04, 0.5))
    ax1.set_ylim(bottom=-0.004)
    ax1.set_ylabel(r'number densities ($\AA^{-3}$)')
    ax1.set_xlabel(r'distance from membrane center ($\AA$)')
    fig1.savefig('plot_raw.png', bbox_inches = 'tight')

    if scale_component:
        ax2.legend(loc=(1.04, 0.5))
        fig2.savefig('plot_scaled.png', bbox_inches = 'tight')

    print("\n\nThe x limits on this plot are {}\n\n".format(plt.gca().get_xlim()))
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

