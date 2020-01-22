
import os
import sys
import numpy as np
import numpy_indexed as npi

def main(infile, outfile, column):

    # load data
    xdata, ydata  = np.loadtxt(args.infile, usecols=(0, column), unpack=True)

    # round the xdata to four decimal places
    xdata = np.round_(xdata, 4)

    # average the values having same abs(x) gridpoint
    rhs_x, rhs_y = npi.group_by(np.abs(xdata)).mean(ydata)

    # regenerate -x data from averaged values (stored in +x side)
    full_x = np.concatenate((np.flip(-rhs_x), rhs_x))
    full_y = np.concatenate((np.flip( rhs_y), rhs_y))

    # remove the -0.0 entry if it exists
    first_neg_idx = len(rhs_x)-1
    if (rhs_x[0] == 0.0) and (full_y[first_neg_idx] == full_y[len(rhs_x)]):
        full_x = np.delete(full_x, first_neg_idx)
        full_y = np.delete(full_y, first_neg_idx)

    # save to file
    np.savetxt(outfile, np.column_stack((full_x, full_y)), delimiter='\t', fmt='%10.4f %10.10f')

if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--infile", required=True,
                        help="Filename of data to be symmetrized.")

    parser.add_argument("-o", "--outfile", required=True,
                        help="Name of the output file.")

    parser.add_argument("-c", "--column", default=1, type=int,
                        help="0-indexed column to symmetrize. Default is 1 (second column).")

    args = parser.parse_args()
    opt = vars(args)
    if os.path.exists(args.outfile):
        sys.exit("ERROR: output file already exists")

    main(args.infile, args.outfile, args.column)

