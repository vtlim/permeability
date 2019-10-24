
import numpy as np
import numpy_indexed as npi
from scipy import integrate

# TODO: consider making the plotting lines in the main function more modular
# TODO: check that file exists in __init__
# TODO: add diagram from group meeting to Github

class Profile:
    def __init__(self, infile, xdata, ydata):
        # if xdata and ydata are NOT passed, initiate object from file
        if all(i is None for i in [xdata, ydata]):
            # only unpack x and y data (ignoring error column if present)
            xdata, ydata = np.genfromtxt(infile, usecols = (0, 1), unpack=True)
        self._infile = infile
        self._xdata = xdata
        self._ydata = ydata

    @property
    def infile(self):
        """Getter for infile."""
        return self._infile

    @property
    def xdata(self):
        """Getter for xdata."""
        return self._xdata

    @property
    def ydata(self):
        """Getter for ydata."""
        return self._ydata

    @infile.setter
    def infile(self, value):
        """Setter for infile."""
        self._infile = value

    @xdata.setter
    def xdata(self, value):
        """Setter for xdata."""
        self._xdata = value

    @ydata.setter
    def ydata(self, value):
        """Setter for ydata."""
        self._ydata = value

    def _decompose_list(list_of_objs):
        """Combine all xdata and ydata from multiple Grad or Pmf objects."""

        # extract data from objects
        whole_i = []
        whole_x = []
        whole_y = []
        for obj in list_of_objs:
            whole_i.append(obj.infile)
            whole_x.append(obj.xdata)
            whole_y.append(obj.ydata)

        # concatenate full list to numpy array
        x = np.concatenate(whole_x)
        grad = np.concatenate(whole_y)

        # concatenate file names into single string
        infilestring = " ".join(whole_i)

        return x, grad, infilestring

    def _sort_by_x(self):
        """Make sure data is sorted by x in ascending order.
        To have descending, use [::-1] after arr1inds."""

        unsorted_x = self.xdata
        unsorted_y = self.ydata

        arr1inds = unsorted_x.argsort()
        sorted_x = unsorted_x[arr1inds]
        sorted_y = unsorted_y[arr1inds]

        self.xdata = sorted_x
        self.ydata = sorted_y

    @staticmethod
    def _get_kt(T):
        """Compute thermal energy."""
        # Boltzmann constant in kcal/(mol K)
        kb = 0.0019872041
        kt = kb*T

        return kt

    def write_data(self, outfile, errbar=False):
        header = "Input data: {}".format(self.infile)

        if errbar:
            np.savetxt(
                outfile, np.c_[self.xdata, self.ydata, self.errbar],
                header=header, fmt=['%.2f', '%.6f', '%.6f'])
        else:
            np.savetxt(
                outfile, np.c_[self.xdata, self.ydata],
                header=header, fmt=['%.2f', '%.6f'])


class Grad(Profile):

    def __init__(self, infile=None, xdata=None, ydata=None):
        super().__init__(infile, xdata, ydata)

    def integrate(self):

        # integrate ydata
        y_pmf = integrate.cumtrapz(self.ydata, self.xdata)

        # take midpoint of all adjacent data points in half_cvs due to integration
        # https://tinyurl.com/ycahltpp
        x_pmf = (self.xdata[1:] + self.xdata[:-1]) / 2
        x_pmf = x_pmf.flatten()

        # create new pmf object from integrated data
        new_pmf = Pmf(self.infile, x_pmf, y_pmf)

        return new_pmf

    @staticmethod
    def join_windows(list_grads):
        """Join windows by averaging overlapping regions of .czar.grad files.
        https://stackoverflow.com/questions/41821539/calculate-average-of-y-values-with-different-x-values

        Parameters
        ----------
        list_grads : list
            list of Grad objects to be combined

        Returns
        -------
        new_grad : Grad
            new Grad object with xdata and ydata of combined grads
        """

        # combine all xdata and all ydata
        x, grad, allfiles = Profile._decompose_list(list_grads)

        # average the values having same x gridpoint
        x_unique, grad_mean = npi.group_by(x).mean(grad)

        # create new grad instance for joined data
        new_grad = Grad(allfiles, x_unique.flatten(), grad_mean.flatten())

        # reorder data for ascending x, then return object
        new_grad._sort_by_x()
        return new_grad


class Pmf(Profile):

    def __init__(self, infile=None, xdata=None, ydata=None):
        super().__init__(infile, xdata, ydata)

    def shift_bulk_zero(self, x0, x1):
        """Compute average from x0 to x1, and shift the average to zero.

        Parameters
        ----------
        x0 : float
        x1 : float

        """
        # get indices of x0 and x1 values
        try:
            x0_index = np.where(np.isclose(self.xdata, x0))[0][0]
            x1_index = np.where(np.isclose(self.xdata, x1))[0][0]
        except IndexError as e:
            raise Exception("ERROR: at least one x-value not found or was " +
                "found more than one time (IndexError)") from e

        # calculate the mean of the region
        orig_mean = np.mean(
            self.ydata[ min(x0_index, x1_index):max(x0_index, x1_index)+1 ])
        print("Unshifted mean from {:6.2f} to {:6.2f} == {:10.4f} kcal/mol".format(x0, x1, orig_mean))

        # shift the y-data
        shifted_ydata = self.ydata - orig_mean
        self.ydata = shifted_ydata

    def symmetrize(self):

        # average the values having same abs(x) gridpoint
        rhs_x, rhs_y = npi.group_by(np.abs(self.xdata)).mean(self.ydata)

        # regenerate -x data from averaged values (stored in +x side)
        full_x = np.concatenate((np.flip(-rhs_x), rhs_x))
        full_y = np.concatenate((np.flip( rhs_y), rhs_y))

        # remove the -0.0 entry if it exists
        first_neg_idx = len(rhs_x)-1
        if (rhs_x[0] == 0.0) and (full_y[first_neg_idx] == full_y[len(rhs_x)]):
            full_x = np.delete(full_x, first_neg_idx)
            full_y = np.delete(full_y, first_neg_idx)

        # compute difference before and after symmetrization
        if not np.array_equal(self.xdata, full_x):
            print("   error in subtracting pmfs before/after symmetrization" +
                "\n   the x-range differs here:\n   " +
                np.setdiff1d(self.xdata, full_x))
        else:
            subtracted = np.abs(self.ydata - full_y)
            self.errbar = subtracted

        # set data in object
        self.xdata = full_x
        self.ydata = full_y


    @staticmethod
    def join_leaflets(list_pmfs, T):
        """Join PMFs by eq. 5 of the following work.
        https://pubs.acs.org/doi/10.1021/jp7114912

        Parameters
        ----------
        list_pmfs : list
            list of the two Pmf objects to be combined
        T : float
            temperature of the system

        Returns
        -------
        new_pmf : Pmf
            new Pmf object with xdata and ydata of combined pmfs
        """

        kt = Profile._get_kt(T)

        # combine all xdata and all ydata
        if len(list_pmfs) != 2:
            print("ERROR: More than 2 PMFs passed into join_leaflets function")
            return
        x, pmf_raw, allfiles = Profile._decompose_list(list_pmfs)

        # take boltzmann weight of free energies
        pmf_boltz = np.exp(-1*pmf_raw/kt)

        # sum overlapping regions
        # https://stackoverflow.com/questions/41821539/calculate-average-of-y-values-with-different-x-values
        x_unique, pmf_boltz_sum = npi.group_by(x).sum(pmf_boltz)

        # calculate free energies from boltzmann sum
        pmf_final = -1*kt*np.log(pmf_boltz_sum)

        # create new pmf instance for joined data
        new_pmf = Pmf(allfiles, x_unique, pmf_final)

        # reorder data for ascending x, then return object
        new_pmf._sort_by_x()
        return new_pmf

    def subsample_errors(self, every_nth):
        "Only keep every Nth value of error values."""
        size = len(self.errbar)
        zeroes = np.zeros(size)

        # get indices which should be kept
        keep_idx = range(0, size, every_nth)

        # transfer the to-keep values into the array of zeros
        zeroes[keep_idx] = self.errbar[keep_idx]
        self.errbar = zeroes

    @staticmethod
    def calc_pka_shift(list_pmfs, T):
        """Compute pKa shift profile by eq. 18 of the following work.
        https://pubs.acs.org/doi/10.1021/jp7114912

        Parameters
        ----------
        list_pmfs : list
            list of the two Pmf objects, FIRST neutral and SECOND charged
        T : float
            temperature of the system

        Returns
        -------
        new_pka : Pka
            new Pka object with xdata and ydata of pKa shift profile
        """

        # extract constants and data
        kt = Profile._get_kt(T)
        x0 = list_pmfs[0].xdata
        x1 = list_pmfs[1].xdata
        y0 = list_pmfs[0].ydata
        y1 = list_pmfs[1].ydata

        # concatenate file names into single string
        allfiles = " ".join([list_pmfs[0].infile, list_pmfs[1].infile])

        # make sure xdata are equal for both
        if len(list_pmfs) != 2:
            print("ERROR: More than 2 PMFs passed into join_leaflets function")
            return
        if not np.array_equal(x0, x1):
            print("   error in matching x-range for computing pka shift " +
                "\n   the x-range differs here:\n   " +
                np.setdiff1d(x0, x1))

        # subtract pmf_neutral minus pmf_charged
        dy = y0 - y1

        # divide by 2.3*kt
        dy = dy/(2.3*kt)

        # create new pmf instance for joined data
        new_pka = Pka(allfiles, x0, dy)

        return new_pka


class Pka(Profile):
    def __init__(self, infile=None, xdata=None, ydata=None):
        super().__init__(infile, xdata, ydata)


def open_join_grads(list_files):
    """Open a list of files with .grad data and join the windows.
    Should this be a static function? Maybe it doesn't make sense to call
    Grad.open_join_grads(...) so maybe better off as module-level function.
    """
    list_grads = []
    for f in list_files:
        g = Grad(f)
        list_grads.append(g)
    joined_grad = Grad.join_windows(list_grads)
    pmf = joined_grad.integrate()

    return pmf


def grads_to_pmf(
    side0_files, side1_files,
    bulk_range0, bulk_range1,
    T,
    out_file='pmf.dat'):

    """Main function to generate symmetrized PMF given input gradient files.

    Parameters
    ----------
    side0_files : list
        list of strings of filenames for gradient files of one side leaflet
    side1_files : list
        list of strings of filenames for gradient files of one side leaflet
    bulk_range0 : list
        list of floats for x values that define bulk region for side0 PMF
    bulk_range1 : list
        list of floats for x values that define bulk region for side1 PMF
    T : float
        temperature of the system
    out_file : string
        filename of the output pmf data

    Returns
    -------
    pmf_0 : Pmf
        new Pmf object of side0
    pmf_1 : Pmf
        new Pmf object of side1
    joined_pmf : Pmf
        new Pmf object with xdata and ydata of joined PMF
    """
    # combine windows of each leaflet
    pmf_0 = open_join_grads(side0_files)
    pmf_1 = open_join_grads(side1_files)

    # shift bulk water region to have average pmf of zero
    pmf_0.shift_bulk_zero(*bulk_range0)
    pmf_1.shift_bulk_zero(*bulk_range1)
    print("Value of pre-shifted bulk water region may be an artifact of where "
          "(x-value) integration begins, where y-value is defined 0.\n")
    pmf_0.write_data('pmf0.dat')
    pmf_1.write_data('pmf1.dat')

    # combine upper and lower leaflets
    joined_pmf = Pmf.join_leaflets([pmf_0, pmf_1], T)

    # symmetrize pmf
    joined_pmf.symmetrize()

    # write out pmf
    joined_pmf.write_data('pmf.dat', errbar=True)

    return pmf_0, pmf_1, joined_pmf

def pmfs_to_pka(pmf0_file, pmf1_file, T, out_file='pka_shift.dat'):
    """Main function to calculate pKa shift profile given 2 files of PMFs.

    Parameters
    ----------
    pmf0_file : string
        filename of the neutral PMF
    pmf1_file : string
        filename of the charged PMF
    T : float
        temperature of the system
    out_file : string
        filename of the output pKa shift profile data

    Returns
    -------
    pka_shift : Pka
        new Pka object with xdata and ydata of pKa shift profile
    """

    pmf_neu = Pmf(pmf0_file)
    pmf_chg = Pmf(pmf1_file)
    pka_shift = Pmf.calc_pka_shift([pmf_neu, pmf_chg], T)
    pka_shift.write_data(out_file)

    return pka_shift


if __name__ == "__main__":

    import argparse
    import matplotlib.pyplot as plt
    parser = argparse.ArgumentParser()

    parser.add_argument("-0", "--side0", required=True, nargs='+',
                        help="One or more files to be processed for one leaflet.")

    parser.add_argument("-1", "--side1", required=True, nargs='+',
                        help="One or more files to be processed for other leaflet.")

    parser.add_argument("-p", "--pka", action="store_true", default=False,
                        help="Compute pKa shift profile from neutral PMF in -0"
                             " flag and charged PMF in -1 flag")

    args = parser.parse_args()

    # compute pka shift profile
    if args.pka and len(args.side0)==1 and len(args.side1)==1:
        pka_shift = pmfs_to_pka(args.side0[0], args.side1[0], T = 295)

        # plot final data
        plt.plot(pka_shift.xdata, pka_shift.ydata)
        plt.grid()
        plt.show()

    # generate pmf from gradient files
    else:
        pmf_0, pmf_1, joined_pmf = grads_to_pmf(
            args.side0, args.side1,
            bulk_range0 = [35, 39.9], bulk_range1 = [-35, -39.9],
            T = 295)

        # for plotting: only keep every Nth error bar else hard to interpret
        joined_pmf.subsample_errors(every_nth = 20)

        # plot final data
        plt.errorbar(joined_pmf.xdata, joined_pmf.ydata, yerr=joined_pmf.errbar)
        plt.plot(pmf_0.xdata, pmf_0.ydata)
        plt.plot(pmf_1.xdata, pmf_1.ydata)
        plt.grid()
        plt.show()
