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

bc = 'NNNN'
path = "/Users/MaoLin/Dropbox/Physics_Research/Quench/fermion_EE/bcft_paper/data/" + bc + "/"
fig_path = "/Users/MaoLin/Dropbox/Physics_Research/Quench/fermion_EE/bcft_paper/images/"
figname = fig_path + bc +"_fit.pdf"

dataset = []
for (dirpath, dirnames, filenames) in walk(path):
    dataset.extend(filenames)

# ----------------------------------------------------------------------           
#                         error bar and slope                          |           
# ----------------------------------------------------------------------
filename=[]
slope=[]
error=[]
for filename in dataset:
    if filename[0]=='.':
        continue
    x = []
    y = []
    for line in open( path + filename ):
        xx, yy = map(float,line.split() )
        x.append( xx )
        y.append( yy )
    if filename==dataset[1]: # for inset
        x_inset=x
        y_inset=y
    slope_array = []
    f = lambda x, a, b: a * x ** b
    for i in range(0,5): # fit five times
        start = randint(0,5)
        x_fit = x[len(x)-start-10 : len(x)-start]
        y_fit = y[len(x)-start-10 : len(x)-start]
        p , c = scipy.optimize.curve_fit( f, x_fit , y_fit )
        slope_array.append( p[1] )
    slope.append( np.mean( slope_array ) )
    error.append( np.std( slope_array ) ) 
# print slope    
# print error    
    
# Print the slope and error bar into a file

# ---------------------------------------------------------------------- 
#                           plot and insets                            |
# ---------------------------------------------------------------------- 

fig, ax = plt.subplots( 1, 1, squeeze = True, figsize = ( 4.5, 3 ) )

theta = np.linspace( 0.5/len(slope) , 0.5 , len(slope) )
ax.plot( theta , slope , 'o', markersize = 3, c = 'blue', label = "numerical" )
ax.plot( theta , np.full((len(slope), 1), -0.25) , c = 'red' , label = "analytical" )

# These are in unitless percentages of the figure size. (0,0 is bottom left)
left, bottom, width, height = [0.35, 0.47, 0.55, 0.4]

ax2 = fig.add_axes([left, bottom, width, height])
ax2.plot( x_inset, y_inset , 'o' , markersize = 2 )    

# ----------------------------------------------------------------------           
#                         title label and axis                         |           
# ----------------------------------------------------------------------

ax.set_xlim( ( 0, 0.5 ) )
ax.set_ylim( ( -0.3, 0 ) )
ax.set_xlabel( r"$\frac{\theta}{\pi}$" )
ax.set_ylabel( r"Slope of echo" )
ax.errorbar( theta , slope , yerr=error , fmt='k.') 
ax.legend( loc = 'best', frameon = False, prop = {'size':6}, ncol=2, handlelength=3 )

ax2.set_yscale('log') 
ax2.set_xscale('log')
ax2.set_xlabel( r"$t$" )
ax2.set_ylabel( r"$\mathcal{L}(t)$" )
 
plt.tight_layout()

fig.savefig( figname )

