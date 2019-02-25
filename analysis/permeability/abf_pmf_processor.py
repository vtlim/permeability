
import numpy as np
import numpy_indexed as npi
from scipy import integrate

# TODO: Add input file data to header from combining windows and for leaflets

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
        whole_x = []
        whole_y = []
        for obj in list_of_objs:
            whole_x.append(obj.xdata)
            whole_y.append(obj.ydata)

        # concatenate full list to numpy array
        x = np.concatenate(whole_x)
        grad = np.concatenate(whole_y)

        return x, grad

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

    def write_data(self, outfile):
        header = "Input data: {}".format(self.infile)
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
        x, grad = Profile._decompose_list(list_grads)

        # average the values having same x gridpoint
        x_unique, grad_mean = npi.group_by(x).mean(grad)

        # create new grad instance for joined data
        new_grad = Grad()
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
            x0_index = np.where(self.xdata==x0)[0][0]
            x1_index = np.where(self.xdata==x1)[0][0]
        except IndexError as e:
            raise Exception("ERROR: at least one x-value not found or was " +
                "found more than one time (IndexError)") from e

        # calculate the mean of the region
        orig_mean = np.mean(
            self.ydata[ min(x0_index, x1_index):max(x0_index, x1_index)+1 ])
        print("Unshifted mean from {} to {} == {}".format(x0, x1, orig_mean))

        # shift the y-data
        shifted_ydata = self.ydata - orig_mean
        self.ydata = shifted_ydata

    def symmetrize(self):

        # average the values having same abs(x) gridpoint
        x, y = npi.group_by(np.abs(self.xdata)).mean(self.ydata)

        # regenerate -x data from averaged values (stored in +x side)
        full_x = np.concatenate((np.flip(-x),x))
        full_y = np.concatenate((np.flip( y),y))

        # set data in object
        self.xdata = full_x
        self.ydata = full_y


    @staticmethod
    def join_leaflets(list_pmfs, temperature):

        # Boltzmann constant in kcal/(mol K)
        kb = 0.0019872041
        kt = kb*temperature

        # combine all xdata and all ydata
        x, pmf_raw = Profile._decompose_list(list_pmfs)

        # take boltzmann weight of free energies
        pmf_boltz = np.exp(-1*pmf_raw/kt)

        # sum overlapping regions
        # https://stackoverflow.com/questions/41821539/calculate-average-of-y-values-with-different-x-values
        x_unique, pmf_boltz_sum = npi.group_by(x).sum(pmf_boltz)

        # calculate free energies from boltzmann sum
        pmf_final = -1*kt*np.log(pmf_boltz_sum)

        # create new pmf instance for joined data
        new_pmf = Pmf()
        new_pmf.xdata = x_unique
        new_pmf.ydata = pmf_final

        # reorder data for ascending x, then return object
        new_pmf._sort_by_x()
        return new_pmf

