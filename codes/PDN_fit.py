#!/bin/env python3
# ----------------------------------------------------------------------- 
#                                header                                 |
# ----------------------------------------------------------------------- 
import glob
from os import walk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib import rcParams
import scipy.optimize
import scipy.stats


rc( 'font', **{'family': 'serif', 'serif': ['Computer Modern'], 'size' : 10} )
rc( 'text', usetex = True )
rcParams['legend.numpoints'] = 1
rcParams['axes.linewidth'] = 0.5
colorList={0:"#ff2222", 1:'#ffa500', 2:'#4488ff', 3:"#0000aa", 4:'#66bb22'}

folder = 'PDN'
path = "../data/" + folder + "/"
fig_path = "../images/"
figname = fig_path + folder + "_fit.pdf"

# get all the filenames in the subdirectory
dataset = []
for ( dirpath, dirnames, filenames ) in walk( path ):
    dataset.extend( filenames )
print( dataset )

# ----------------------------------------------------------------------
#                         error bar and slope                          |           
# ----------------------------------------------------------------------
def fit_data( x, y ):

    log_x = np.log( x ) / np.log( 10 )
    log_y = np.log( y ) / np.log( 10 )

    data_range = np.logical_and( log_x > 0, log_x < 2 )
    log_x = log_x[ data_range ]
    log_y = log_y[ data_range ]

    slope, _, _, _, std_err = scipy.stats.linregress( log_x, log_y )

    error = std_err

    return -slope, error 

slope = []
error = []
x = []

for filename in dataset:
    data = np.loadtxt( path + filename )
    t = data[:,0]
    echo = data[:,1]

    # extract x = theta / pi from filename
    x.append( float( filename.split('_')[0] ) )
    
    this_slope, this_error = fit_data( t, echo );
    slope.append( this_slope )
    error.append( this_error )

# sort index
x = np.array( x )
slope = np.array( slope )
error = np.array( error )
idx = np.argsort( x )
x = x[idx]
slope = slope[idx]
error = error[idx]

# inset data
inset_x = [1, 5, 40]
t_inset = []
echo_inset = []
for i in inset_x:
    inset_data = np.loadtxt( path + dataset[i] )
    t_inset.append( inset_data[:,0] )
    echo_inset.append( inset_data[:,1] )

# ---------------------------------------------------------------------- 
#                           plot and insets                            |
# ---------------------------------------------------------------------- 

fig, ax = plt.subplots( 1, 1, squeeze = True, figsize = ( 4.5, 3 ) )
# analytic results
x_analy = np.insert( x, 0, 0 )
y_analy = 2 * ( -np.square( x_analy ) + x_analy )
ax.plot( x_analy, y_analy, color = 'red' , label = r"analytical $\frac{\theta}{\pi} - \left(\frac{\theta}{\pi}\right)^2$" )
ax.plot( x_analy, y_analy-1.0/8, color = 'green' , label = r"$\frac{\theta}{\pi} - \left(\frac{\theta}{\pi}\right)^2-\frac{1}{8}$" )

# numerical results
(_, caps, _) = ax.errorbar( x, slope, yerr = error, fmt='o', color = 'black', capsize = 1, markersize = 1, label = "numerical" ) 
for cap in caps:
    cap.set_markeredgewidth( 0.5 )


# ----------------------------------------------------------------------           
#                         title label and axis                         |           
# ----------------------------------------------------------------------

ax.set_xlim( ( 0, 0.5 ) )
ax.set_ylim( ( 0, 0.6 ) )
ax.set_xlabel( r"$\frac{\theta}{\pi}$" )
ax.set_ylabel( r"Echo Exponent" )
ax.legend( loc = 'upper left', frameon = False, prop = {'size':6}, ncol = 1, handlelength = 3 )

# plt.tight_layout()

fig.savefig( figname, bbox_inches = 'tight' )
