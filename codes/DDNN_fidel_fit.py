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

folder = 'DDNN_fidel'
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

    data_range = ( log_x < 4 )
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
    L = data[:,0]
    F = data[:,1]

    # extract x = theta / pi from filename
    x.append( float( filename ) )
    
    this_slope, this_error = fit_data( L, F );
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
L_inset = []
F_inset = []
for i in inset_x:
    inset_data = np.loadtxt( path + dataset[i] )
    L_inset.append( inset_data[:,0] )
    F_inset.append( inset_data[:,1] )

# ---------------------------------------------------------------------- 
#                           plot and insets                            |
# ---------------------------------------------------------------------- 

fig, ax = plt.subplots( 1, 1, squeeze = True, figsize = ( 4.5, 3 ) )
# analytic results
x_analy = np.insert( x, 0, 0 )
y_analy = ( -np.square( x_analy ) + x_analy )
ax.plot( x_analy, y_analy, color = 'red' , label = r"analytical $\frac{\theta}{\pi} - \left(\frac{\theta}{\pi}\right)^2$" )

# numerical results
(_, caps, _) = ax.errorbar( x, slope, yerr = error, fmt='o', color = 'black', capsize = 1, markersize = 2, label = "numerical" ) 
for cap in caps:
    cap.set_markeredgewidth( 1 )

# inset position
left, bottom, width, height = [0.55, 0.27, 0.3, 0.25]
ax2 = fig.add_axes( [left, bottom, width, height] )

for i in range( 0, len( inset_x ) ):
    ax2.plot( L_inset[i], F_inset[i] , 'o' , markersize = 1.5, c = colorList[i] )

# ----------------------------------------------------------------------           
#                         title label and axis                         |           
# ----------------------------------------------------------------------

ax.set_xlim( ( 0, 0.5 ) )
ax.set_ylim( ( 0, 0.3 ) )
ax.set_xlabel( r"$\frac{\theta}{\pi}$" , fontsize=15)
ax.set_ylabel( r"Fidelity Exponent" )
ax.legend( loc = 'upper left', frameon = False, prop = {'size':10}, ncol = 1, handlelength = 3 )

# smaller font for inset
for tick in ax2.xaxis.get_major_ticks():
    tick.label.set_fontsize( 8 )
for tick in ax2.yaxis.get_major_ticks():
    tick.label.set_fontsize( 8 )

ax2.set_yscale( 'log' ) 
ax2.set_xscale( 'log' )
ax2.set_xlabel( r"$L$", fontsize = 8 )
ax2.set_ylabel( r"Fidelity", fontsize = 8 )
ax2.yaxis.set_ticks( np.linspace( 0.001, 0.1, 2 ) )
ax2.yaxis.set_label_coords( -0.1, 0.5 )
 
# plt.tight_layout()

fig.savefig( figname, bbox_inches = 'tight' )
