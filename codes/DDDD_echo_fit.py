#!/bin/env python3
# ----------------------------------------------------------------------- 
#                                header                                 |
# ----------------------------------------------------------------------- 
import glob
from os import walk
from math import pi, exp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib import rcParams
import scipy.stats
from random import randint

rc( 'font', **{'family': 'serif', 'serif': ['Computer Modern'], 'size' : 10} )
rc( 'text', usetex = True )
rcParams['legend.numpoints'] = 1
rcParams['axes.linewidth'] = 0.5
colorL={6:"#ff2222", 8:'#ffa500', 10:'#4488ff', 12:"#0000aa", 14:'#66bb22'}

bc = 'DDDD' 
path = "../data/" + bc + "/"
fig_path = "../images/"
figname = fig_path + bc +"_fit.pdf"

offset=0

dataset = []
for (dirpath, dirnames, filenames) in walk(path):
    dataset.extend(filenames)
# print dataset

# ----------------------------------------------------------------------           
#                         error bar and slope                          |           
# ----------------------------------------------------------------------


def fit_data( x, y ):

    log_x = np.log( x ) / np.log( 10 )
    log_y = np.log( y ) / np.log( 10 )

    log_x = log_x[ x > 20 ]
    log_y = log_y[ x > 20 ]
    
    # std_err is already the error of the slope!
    slope, _, _, _, std_err = scipy.stats.linregress( log_x, log_y )

    error = std_err

    return -slope, error 

slope = []
error = []
x = []

for filename in dataset:
   if filename[0]=='.':
       continue
   data = np.loadtxt( path + filename )
   t = data[:,0]
   echo = data[:,1]

   # extract x = theta / pi from filename
   x.append( float( filename.split('_')[1] ) )
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
print( idx )


# print x
# print slope
# print error

inset_data = np.loadtxt( path + dataset[idx[0]] )
t_inset = inset_data[:,0]
echo_inset = inset_data[:,1] 

# ---------------------------------------------------------------------- 
#                           plot and insets                            |
# ---------------------------------------------------------------------- 

fig, ax = plt.subplots( 1, 1, squeeze = True, figsize = ( 4.5, 3 ) )

x_analy = np.insert( x, 0, 0 )
y_analy = np.full((len(x_analy), 1), 0.25)

ax.plot( x_analy ,  y_analy, c = 'red' , lw=1 , label = "analytical" )
(_, caps, _) = ax.errorbar( x, slope, yerr = error, fmt='o', color = 'black', capsize = 1, markersize = 2, label = "numerical" ) 
for cap in caps:
  cap.set_markeredgewidth( 1 )

left, bottom, width, height = [0.25, 0.2, 0.60, 0.4]
ax2 = fig.add_axes([left, bottom, width, height])
ax2.loglog( t_inset, echo_inset , 'o' , markersize = 1, color = 'blue' )
ax2.loglog( t_inset[20:-1], (t_inset[20:-1])**(-0.25) / 2, 'k--', lw = 0.25, dashes = (5, 5) )
# ax2.annotate("$t^{-0.25}$", xy=(0.5, 0.3), xycoords='axes fraction' ,horizontalalignment='left', verticalalignment='bottom' )
ax2.annotate("$t^{-0.25}$", xy=(0.1,0.1), xytext=(1.5, 0.2) ,horizontalalignment='left', verticalalignment='bottom' )


# ----------------------------------------------------------------------           
#                         title label and axis                         |           
# ----------------------------------------------------------------------

ax.set_xlim( ( 0, 0.5 ) )
ax.set_ylim( ( 0 , 0.3 ) )
ax.set_xlabel( r"$\frac{\theta}{\pi}$" )
ax.set_ylabel( r"Echo Exponent" )
ax.legend( loc = 'upper left', frameon = False, prop = {'size':6}, ncol = 1, handlelength = 3 )


# smaller font for inset
for tick in ax2.xaxis.get_major_ticks():
    tick.label.set_fontsize( 8 )
for tick in ax2.yaxis.get_major_ticks():
    tick.label.set_fontsize( 8 )

ax2.set_yscale('log')
ax2.set_xscale('log')
ax2.set_xlabel( r"$t$" , fontsize=8 )
ax2.set_ylabel( r"Loschmidt Echo" , fontsize = 8 )

ax2.set_xlim( ( 0.01 , 1000 ) )
# ax2.xaxis.set_ticks(np.linspace( 0.01 , 1000 , 2 ))
ax2.yaxis.set_ticks(np.linspace( 0.1 , 1 , 2 ))
ax2.xaxis.set_label_coords(0.5, -0.025)
ax2.yaxis.set_label_coords(-0.05, 0.5)

fig.savefig( figname, bbox_inches = 'tight' )

