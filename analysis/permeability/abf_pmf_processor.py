
import numpy as np
import numpy_indexed as npi
from scipy import integrate

class Profile:
    def __init__(self, infile):
        if infile is not None:
            xdata, ydata = np.genfromtxt(infile, unpack=True)
        else:
            xdata = None
            ydata = None
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

    def write_data(self, outfile, errbar=False):
        header = "Input data: {}".format(self.infile)

        if errbar:
            np.savetxt(
                outfile, np.c_[self.xdata,self.ydata,self.errbar],
                header=header, fmt=['%.2f','%.6f','%.6f'])
        else:
            np.savetxt(
                outfile, np.c_[self.xdata,self.ydata],
                header=header, fmt=['%.2f','%.6f'])

class Grad(Profile):

    def __init__(self, infile=None):
        Profile.__init__(self, infile)

    def integrate(self):

        # integrate ydata
        y_pmf = integrate.cumtrapz(self.ydata, self.xdata)

        # take midpoint of all adjacent data points in half_cvs due to integration
        # https://tinyurl.com/ycahltpp
        x_pmf = (self.xdata[1:] + self.xdata[:-1]) / 2
        x_pmf = x_pmf.flatten()

        # create new pmf object from integrated data
        new_pmf = Pmf()
        new_pmf.infile = self.infile
        new_pmf.xdata = x_pmf
        new_pmf.ydata = y_pmf

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
        new_grad = Grad()
        new_grad.infile = allfiles
        new_grad.xdata = x_unique.flatten()
        new_grad.ydata = grad_mean.flatten()

        # reorder data for ascending x, then return object
        new_grad._sort_by_x()
        return new_grad

class Pmf(Profile):

    def __init__(self, infile=None):
        Profile.__init__(self, infile)

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
        print("Unshifted mean from {} to {} == {:10.4f}".format(x0, x1, orig_mean))

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
                "\n   the xrange differs here:\n   " +
                np.setdiff1d(self.xdata, full_x))
        else:
            subtracted = np.abs(self.ydata - full_y)
            self.errbar = subtracted

        # set data in object
        self.xdata = full_x
        self.ydata = full_y


    @staticmethod
    def join_leaflets(list_pmfs, temperature):
        """Join PMFs by eq. 5 of the following work.
        https://pubs.acs.org/doi/10.1021/jp7114912

        Parameters
        ----------
        list_pmfs : list
            list of the two Pmf objects to be combined

        Returns
        -------
        new_pmf : Pmf
            new Pmf object with xdata and ydata of combined pmfs
        """

        # Boltzmann constant in kcal/(mol K)
        kb = 0.0019872041
        kt = kb*temperature

        # combine all xdata and all ydata
        x, pmf_raw, allfiles = Profile._decompose_list(list_pmfs)

        # take boltzmann weight of free energies
        pmf_boltz = np.exp(-1*pmf_raw/kt)

        # sum overlapping regions
        # https://stackoverflow.com/questions/41821539/calculate-average-of-y-values-with-different-x-values
        x_unique, pmf_boltz_sum = npi.group_by(x).sum(pmf_boltz)

        # calculate free energies from boltzmann sum
        pmf_final = -1*kt*np.log(pmf_boltz_sum)

        # create new pmf instance for joined data
        new_pmf = Pmf()
        new_pmf.infile = allfiles
        new_pmf.xdata = x_unique
        new_pmf.ydata = pmf_final

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

if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument("-0", "--side0", required=True, nargs='+',
                        help="One or more files to be processed for one leaflet.")

    parser.add_argument("-1", "--side1", required=True, nargs='+',
                        help="One or more files to be processed for other leaflet.")

    args = parser.parse_args()

    # combine windows of upper leaflet
    list_grads = []
    for f in args.side0:
        g = Grad(f)
        list_grads.append(g)
    joined_grad = Grad.join_windows(list_grads)
    pmf_top = joined_grad.integrate()

    # combine windows of lower leaflet
    list_grads = []
    for f in args.side1:
        g = Grad(f)
        list_grads.append(g)
    joined_grad = Grad.join_windows(list_grads)
    pmf_bot = joined_grad.integrate()

    # shift bulk water region to have average pmf of zero
    pmf_top.shift_bulk_zero( 35, 39.9)
    pmf_bot.shift_bulk_zero(-35,-39.9)

    # combine upper and lower leaflets
    joined_pmf = Pmf.join_leaflets([pmf_top, pmf_bot], 295)

    # symmetrize pmf
    joined_pmf.symmetrize()

    # write out pmf (this same call can be used on Grad objects)
    joined_pmf.write_data('pmf.dat', errbar=True)

    # for plotting: only keep every Nth error bar else hard to interpret
    joined_pmf.subsample_errors(every_nth = 20)

    # plot final data
    import matplotlib.pyplot as plt
    plt.errorbar(joined_pmf.xdata, joined_pmf.ydata, yerr=joined_pmf.errbar)
    plt.plot(pmf_top.xdata, pmf_top.ydata)
    plt.plot(pmf_bot.xdata, pmf_bot.ydata)
    plt.grid()
    plt.show()
