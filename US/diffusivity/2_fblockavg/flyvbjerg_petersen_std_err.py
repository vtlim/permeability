# Copyright 2014, Jerome Fung, Rebecca W. Perry, Thomas G. Dimiduk
#
# flyvbjerg_petersen_std_err is free software: you can redistribute it 
# and/or modify it under the terms of the GNU General Public License 
# as published by the Free Software Foundation, either version 3 of the 
# License, or (at your option) any later version.
#
# This code is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with flyvbjerg_petersen_std_err.  If not, see 
# <http://www.gnu.org/licenses/>.

'''
Apply Flyvbjerg-Petersen block decorrelation method for estimating the 
standard error on the mean of a (possibly correlated) time series of 
values.

.. moduleauthor:: Jerome Fung <jerome.fung@gmail.com>
.. moduleauthor:: Rebecca W. Perry <rperry@seas.harvard.edu>
.. moduleauthor:: Tom Dimiduk <tom@dimiduk.net>

Reference: H. Flyvbjerg and H. G. Petersen, "Error estimates on correlated
data", J. Chem. Phys. 91, 461--466 (1989).
'''

import numpy as np
import warnings

def block_transformation(series):
    """
    Do a single step of fp block averaging.

    Parameters
    ----------
    series : ndarray
        Things we want to average: e.g. squared displacements to calculate the
        mean squared displacement of a Brownian particle.

    Returns
    -------
    blocked_series : ndarray
        an array of half the length of series with adjacent terms averaged

    Notes
    -----
    Flyvbjerg & Peterson 1989, equation 20

    """
    n_steps = series.size
    n_steps_p = np.floor(n_steps/2.)
    output = 0.5 * (series[::2][:n_steps_p] + series[1::2][:n_steps_p])
    return output

def calculate_blocked_variances(series, npmin = 15):
    """
    Compute a series of blocks and variances.

    Parameters
    ----------
    series : ndarray
        the thing we want to average: e.g. squared
        displacements for a Brownian random walk.
    npmin : int
        cutoff number of points to stop blocking

    Returns
    -------
    output_var, var_stderr : ndarray
        The variance and stderr of the variance at each blocking level

    Notes
    -----
    Flyvbjerg & Peterson suggest continuing blocking down to 2 points, but the
    last few blocks are very noisy, so we default to cutting off before that.

    """
    n_steps = series.size

    def var(d, n):
        # see eq. 27 of FP paper
        return d.var()/(n-1)
    def stderr_var(n):
        # see eq. 27 of FP paper
        return np.sqrt(2./(n-1))

    output_var = np.array([var(series, n_steps)]) # initialize
    var_stderr = np.array([stderr_var(n_steps)])

    while n_steps > npmin:
        series = block_transformation(series)
        n_steps = series.size
        # TODO: precompute size of output_var and var_stderr from n_steps
        # rather than appending
        output_var = np.append(output_var, var(series, n_steps))
        var_stderr = np.append(var_stderr, stderr_var(n_steps))

    return output_var, var_stderr

def detect_fixed_point(fp_var, fp_sev, full_output = False):
    """
    Find whether the block averages decorrelate the data series to a fixed
    point.

    Parameters
    ----------
    fp_var: ndarray
        FP blocked variance
    fp_sev: ndarray
        FP standard error of the variance.

    Returns
    -------
    best_var : float
        best estimate of the variance
    converged : bool
        did the series converge to a fixed point?
    bounds : (int, int) only if full_output is True
        range of fp_var averaged to compute best_var

    Notes
    -----
    Expects both fp_var and fp_sev will have been
    truncated to cut off points with an overly small n_p and
    correspondingly large standard error of the variance.

    """
    n_trans = fp_var.size # number of block transformations and index

    left_index = 0
    right_index = 0

    # Detect left edge
    for i in np.arange(n_trans):
        # ith point inside error bars of next point
        if np.abs(fp_var[i + 1] - fp_var[i]) < fp_var[i + 1] * fp_sev[i + 1]:
            left_index = i
            break

    # Check right edge
    for i in np.arange(n_trans)[::-1]:
        if np.abs(fp_var[i] - fp_var[i - 1]) < fp_var[i - 1] * fp_sev[i - 1]:
            right_index = i
            break

    # if search succeeds
    if (left_index >= 0) and (right_index >= 0) and \
            (right_index >= left_index):
        best_var = np.average(fp_var[left_index:right_index + 1],
                              weights = 1./fp_sev[left_index:right_index + 1])
        converged = True
    else:
        best_var = fp_var.max()
        converged = False

    if full_output is True:
        return best_var, converged, (left_index, right_index)
    else:
        return best_var, converged


def fp_stderr(data):
    '''
    Compute standard error using Flyvbjerg-Petersen blocking.

    Computes the standard error on the mean of a possibly correlated timeseries
    of measurements.

    Parameters
    ----------
    data: ndarray
        data whose mean is to be calculated, and for which we need
        a standard error on the mean

    Returns
    -------
    stderr : float
        Standard error on the mean of data

    Notes
    -----

    Uses the technique described in H. Flyvbjerg and H. G. Petersen,
    "Error estimates on correlated data", J. Chem. Phys. 91, 461--466 (1989).
    section 3.

    '''
    block_trans_var, block_trans_sev = calculate_blocked_variances(data)
    var_mean, conv, bounds = detect_fixed_point(block_trans_var,
                                                block_trans_sev, True)

    if not conv:
        warnings.warn("Fixed point not found, returned value is a lower bound on the standard error")
    return np.sqrt(var_mean)

#  LocalWords:  Flyvbjerg
