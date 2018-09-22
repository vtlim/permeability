/**
 * compile by g++ name.cpp -o executableName 
 * usage is ./correlation trajfile fieldnumber
 *
 * This script reads in one NAMD *.traj file and calculates the autocorrelation function and diffusion coefficient. For umbrella sampling simulations.
 * More explanation on usage: 
 *    'correlation' is the name of the executable C++ file
 *    'trajfile' is NAMD *.traj file
 *    'fieldnumber' is optional parameter specifying column to read from trajfile. 
 *        E.g. Column 0 is timestep, column (field) 1 is position. Default is 1.
 * 
 * REFERENCE
 * Lee, C. T.; Comer, J.; Herndon, C.; Leung, N.; Pavlova, A.; Swift, R. V.; Tung, C.; Rowley, C. N.; Amaro, R. E.; Chipot, C.; Wang, Y.; Gumbart, J. C.Simulation-Based Approaches for Determining Membrane Permeability of Small Compounds J. Chem. Inf. Model. 2016, 56, 721– 733, DOI: 10.1021/acs.jcim.6b00022

*/

#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <cstdlib>
#include <stdlib.h>
#include <vector>
#include <iterator>
#include <algorithm>

using namespace std;


/**
    Calculate the position autocorrelation function of timeseries.

    @param y Timeseries data as vector of doubles. Already subtracted average.
    @param nSamples Number of samples in this timeseries vector.
    @param nCorr                     ???? nsamples in summation of eq 5 ?????
    @return autocorrelation function as a vector of doubles.

*/
double *calcCorrelation(double *y, int nSamples, int nCorr)
{
    double *corr=new double[nCorr];  // correlation as a function of lag time
    int *norm=new int[nCorr];
    int min;
    int t;
    int ttoMax;

    // set initial zero values for all the lag times
    for(int i=0;i<nCorr;++i) {
        corr[i]=0.0;
        norm[i]=0;
    }

    // each value of timeseries is used as reference (the i in eq. 5)
    for(int i=0;i<nSamples;++i) {

        // set upper limit of summation for eq. 5
        // use whichever is smaller, nSamples or i+nCorr
        ttoMax=nSamples;
        if(i+nCorr<nSamples) ttoMax=i+nCorr;

        // for each value of timeseries, calc pdt of incr lag times
        for(int j=i;j<ttoMax;++j) {
            t=j-i;
            corr[t]+=y[i]*y[j];
            norm[t]++;
        }
    }

    // for each of the Czz(t) values, divide by counts (n_samples in eq 5)
    for(int i=0;i<nCorr;++i) {
        corr[i]=corr[i]/norm[i];
    }
    delete[] norm;

    return(corr);
}


/**
    Calculate variance of the timeseries. 
    Variance is the sum of squared differences (x - <x>), divided by N-1.
    The differences should already have been taken. Here, square, add, divide.

    @param y Timeseries data as vector of doubles. Already subtracted average.
    @param nSamples Number of samples in this timeseries vector.
    @return double value of the variance of the time series.

*/
double variance(double *y, int nSamples)
{
    double v2=0.0;
    for(int i=0;i<nSamples;++i)
    v2+=y[i]*y[i];
    // cout << "variance << " << v2 << endl;
    v2/=nSamples; // ???????????????/ N-1 ??????????????
    return(v2);
}

/**
    Take a timeseries vector and transform it into a vector with
    the average subtracted from each component.
                dz(t) = z(t) - <z>

    @param y Timeseries data as vector of doubles. 
    @param nSamples Number of samples in this timeseries vector.

*/
void subtract_average(double *y, int nSamples)
{
    double avg=0.0;

    // add up all the numbers in the timeseries
    for(int i=0;i<nSamples;++i)
        avg+=y[i];

    // divide by total number of counts to get average
    avg/=nSamples;

    // take each value and subtract the average
    for(int i=0;i<nSamples;++i)
        y[i]-=avg;
}


/**
    Integrate the autocorrelation function as in eq. 4.
    Trapezoidal rule: integral from a to b of f(x) =
        (b-a) * [f(a)+f(b)]/2
    where, here, timestep=b-a.

    @param acf autocorrelation function as a vector of doubles.
    @param nCorr length of the autocorrelation function
    @param timestep
    @return double value of the integrated autocorrelation function.

*/
double integrateCorr(double *acf, int nCorr, double timestep)
{
    double I=0;
    for(int i=0;i<nCorr-1;++i) {
        I+=0.5*(acf[i]+acf[i+1])*timestep;
    }

    return(I);
}

/**
    Count number of data lines in the *.traj file.

    @param fname Name of the data file
    @return integer number of data lines in file

*/
int countLines(char *fname)
{
    string line;
    int numSamples=0;
    ifstream datafile(fname);

    while(getline(datafile,line)) {
        if(line.at(0)!='#')
        ++numSamples;
    }

    datafile.close();
    return(numSamples);
}


/**
    Open, read, and return timeseries data from NAMD *.traj file.

    @param fname Name of the timeseries (*.traj) file.
    @param numSamples Reference to variable detailing number of samples within the timeseries file.
    @param field Column number in the NAMD *traj file. E.g. Column 0 is step, column (field) 1 is position.
    @return vector of relevant timeseries data (no timestep)

*/
vector<double> readSeries(char *fname, int &numSamples, int field)
{
    ifstream datafile(fname);
    vector<double> series;
    double *timeSeries;
    int i=0;
    string line;
    istringstream iss;
    int begin;

    if(field==1)
        begin=15;
    else if(field==2)
        begin=37;
    else
        begin=61;

    numSamples=0;
    while(getline(datafile,line))
    {
    //  cout << line << endl;

        // skip lines starting with '#'
        if(line.at(0)!='#')
    {
        // get relevant data starting at char begin, 23 chars long
        string str2=line.substr(begin,23);
        // extend the vector by one
        series.push_back(atof(str2.c_str()));
        // increment numSamples
        ++numSamples;
    }
    }
    return(series);
}

//////////////////////////////////////////////////////////////////

int main(int argc, char *argv[])
{
//    int nCorr=10000; // ?????????????????????????? nSamples / 2
    int nCorr=6000; // ?????????????????????????? nSamples / 2
    vector<double> series;
    double *acf, *timeSeries;
    double var, I;
    char *fname;
    double timestep=2.0;
    int field=1;
    int numSamples;

    // if the number of arguments len(argv) is 0, then quit
    if(argc<1)
        return(1);
    
    // get trajfile name from argument 1
    fname=argv[1];
    
    // get field number from arg 2 and convert to integer
    if(argc>1)    
        field=atoi(argv[2]);
        //  int numSamples=countLines(fname)-1;
    
    // get vector of timeseries data
    series=readSeries(fname, numSamples, field);
    timeSeries=&series[0];
    
    // fix numSamples since readSeries increments one at the end
    numSamples=numSamples-1;

    // transform timeSeries by subtracting avg from each component    
    subtract_average(timeSeries, numSamples);

    // calculate autocorrelation function (vector as fx of lag times)
    acf=calcCorrelation(timeSeries, numSamples, nCorr);

    // get value of variance.
    var=variance(timeSeries, numSamples);

    // get double value of integrated ACF 
    I=integrateCorr(acf, nCorr, timestep);

    // print statistics
    cout << "I = " << I << endl;
    cout << "var = " << var << endl;

    // take var^2 to calculate diffusion coefficient and print
    cout << "D = " << var*var/I << " A2/fs " << endl;
    cout << "D = " << var*var/I*0.1 << " cm2/s " << endl;

    // print the acf
    for(int i=0;i<10;++i)
        cout << i << " " << acf[i] << endl;

    // clean up
    delete[] acf;
//    for( int i = 0 ; i < series.size(); i++)
//       delete series[i];
//       series.clear();
}
