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
from random import randint


rc( 'font', **{'family': 'serif', 'serif': ['Computer Modern'], 'size' : 10} )
rc( 'text', usetex = True )
rcParams['legend.numpoints'] = 1
rcParams['axes.linewidth'] = 0.5

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
    slope_array = []

    f = lambda x, a, b: a * x ** b
    for i in range( 0, 5 ): # fit five times
        start = randint( 0, 5 )
        x_fit = x[len(x)-start-10 : len(x)-start]
        y_fit = y[len(x)-start-10 : len(x)-start]
        p , c = scipy.optimize.curve_fit( f, x_fit , y_fit )
        slope_array.append( -p[1] )

    slope = np.mean( slope_array )
    error = np.std( slope_array )

    return slope, error 

slope = []
error = []
x = []

for filename in dataset:
    data = np.loadtxt( path + filename )
    t = data[:,0]
    echo = data[:,1]

    # extract x = theta / pi from filename
    x.append( float( filename ) )
    
    this_slope, this_error = fit_data( t, echo );
    slope.append( this_slope )
    error.append( this_error )

inset_data = np.loadtxt( path + dataset[1] )
t_inset = inset_data[:,0]
echo_inset = inset_data[:,1]

# ---------------------------------------------------------------------- 
#                           plot and insets                            |
# ---------------------------------------------------------------------- 

fig, ax = plt.subplots( 1, 1, squeeze = True, figsize = ( 4.5, 3 ) )
ax.plot( x, slope, 'o', markersize = 3, c = 'blue', label = "numerical" )
x.append( 0 )
x_analy = sorted( x )
y_analy = ( -np.square( x_analy ) + x_analy )
x = x[:-1]
ax.plot( x_analy, y_analy, c = 'red' , label = "analytical" )

# These are in unitless percentages of the figure size. (0,0 is bottom left)
left, bottom, width, height = [0.55, 0.27, 0.3, 0.25]

ax2 = fig.add_axes( [left, bottom, width, height] )
ax2.plot( t_inset, echo_inset , 'o' , markersize = 2 )    

# ----------------------------------------------------------------------           
#                         title label and axis                         |           
# ----------------------------------------------------------------------

ax.set_xlim( ( 0, 0.5 ) )
ax.set_ylim( ( 0, 0.3 ) )
ax.set_xlabel( r"$\frac{\theta}{\pi}$" )
ax.set_ylabel( r"Fidelity Exponent" )
ax.errorbar( x , slope , yerr = error , fmt = 'k.' ) 
ax.legend( loc = 'best', frameon = False, prop = {'size':6}, ncol = 2, handlelength = 3 )

# smaller font for inset
for tick in ax2.xaxis.get_major_ticks():
    tick.label.set_fontsize( 8 )
for tick in ax2.yaxis.get_major_ticks():
    tick.label.set_fontsize( 8 )

ax2.set_yscale( 'log' ) 
ax2.set_xscale( 'log' )
ax2.set_xlabel( r"$t$", fontsize = 8 )
ax2.set_ylabel( r"$\mathcal{L}(t)$", fontsize = 8 )
 
# plt.tight_layout()

fig.savefig( figname, bbox_inches = 'tight' )

