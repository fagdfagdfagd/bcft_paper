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
import scipy.optimize
from random import randint

rc( 'font', **{'family': 'serif', 'serif': ['Computer Modern'], 'size' : 10} )
rc( 'text', usetex = True )
rcParams['legend.numpoints'] = 1
rcParams['axes.linewidth'] = 0.5
colorL={6:"#ff2222", 8:'#ffa500', 10:'#4488ff', 12:"#0000aa", 14:'#66bb22'}

bc = 'PP' 
path = "../data/" + bc + "/"
fig_path = "../images/"
figname = fig_path + bc +"_fit.pdf"

offset=0.15/25*pi/2/pi

dataset = []
for (dirpath, dirnames, filenames) in walk(path):
    dataset.extend(filenames)
# print dataset

# ----------------------------------------------------------------------           
#                         error bar and slope                          |           
# ----------------------------------------------------------------------
def fit_data( x, y ,where ):
    slope_array = []

    f = lambda x, a, b: a * x ** b
    for i in range( 0, 5 ): # fit five times
        start = randint( 0, 5 )
        if where=='center':
            x_fit = t[40-start-15 : 40-start]
            y_fit = echo[40-start-15 : 40-start]
        elif where=='others':
            x_fit = t[25-start-20 : 25-start]
            y_fit = echo[25-start-20 : 25-start]
        p , c = scipy.optimize.curve_fit( f, x_fit , y_fit )
        slope_array.append( -p[1] )

    slope = np.mean( slope_array )
    error = np.std( slope_array )

    return slope, error 

slope = []
error = []
x = []

for filename in dataset:
   if filename[0]=='.':
       continue
   # extract x = theta / pi from filename
   x.append( float( filename.split('_')[1] ) )

# sort index
x = np.array( x )
idx = np.argsort( x )
x = x[idx]
dataset = np.array( dataset )
print( dataset )
dataset = dataset[idx]
print( dataset )

for filename in dataset:
   data = np.loadtxt( path + filename )
   t = data[:,0]
   echo = data[:,1]
   if filename in dataset[9:14]:
        where='center'
   else:
        where='others'
   this_slope, this_error = fit_data( t, echo , where );
   slope.append( this_slope )
   error.append( this_error )


inset_data = np.loadtxt( path + dataset[1] )
t_inset = inset_data[:,0]
echo_inset = inset_data[:,1]
inset_data = np.loadtxt( path + dataset[4] )
t_inset_2 = inset_data[:,0]
echo_inset_2 = inset_data[:,1]
inset_data = np.loadtxt( path + dataset[9] )
t_inset_3 = inset_data[:,0]
echo_inset_3 = inset_data[:,1]
inset_data = np.loadtxt( path + dataset[12] )


# ---------------------------------------------------------------------- 
#                           plot and insets                            |
# ---------------------------------------------------------------------- 

fig, ax = plt.subplots( 1, 1, squeeze = True, figsize = ( 4.5, 3 ) )

x_analy = np.linspace( 0 , 0.5 , 200 )

y_analy = (-1)*2 * ( np.square([this_x_analy-0.25 for this_x_analy in x_analy]) - [abs(this_x_analy-0.25) for this_x_analy in x_analy] ) 

# y_analy = (-1)*2 * ( np.square(x_analy-0.25) - abs(x_analy-0.25) ) 
ax.plot( x_analy , y_analy , c = 'red' , label = r"analytical $2\left(\frac{\theta}{\pi} - \left(\frac{\theta}{\pi}\right)^2\right)$" )
ax.plot( x , [-this_slope for this_slope in slope] , 'o', markersize = 2, c = 'black', markeredgewidth=0.0 , label = "numerical" )
left, bottom, width, height = [0.41, 0.60, 0.30, 0.3]
ax2 = fig.add_axes([left, bottom, width, height])
ax2.plot( t_inset, echo_inset , 'o' , markersize = 2 , c = colorL[6] , label = r"$\theta=0.02\pi$" )
ax2.plot( t_inset_2, echo_inset_2 , 'o' , markersize = 2 , c = colorL[8] , label = r"$\theta=0.12\pi$" )
ax2.plot( t_inset_3, echo_inset_3 , 'o' , markersize = 2 , c = colorL[10] , label = r"$\theta=0.24\pi$" )
plt.text(0.05, 0.95,'(a)', ha='center', va='center', transform=ax.transAxes)

# ----------------------------------------------------------------------           
#                         title label and axis                         |           
# ----------------------------------------------------------------------

ax.set_xlim( ( 0, 0.5 ) )
ax.set_ylim( ( 0 , 0.4 ) ) 

ax.set_xlabel( r"$\frac{\theta}{\pi}$" )
ax.set_ylabel( r"Echo Exponent" )
ax.errorbar( x , slope , yerr=error , fmt='k.')

ax.legend( loc = 'lower left', frameon = False, prop = {'size':6}, ncol=1, handlelength=3 )

# smaller font for inset
for tick in ax2.xaxis.get_major_ticks():
    tick.label.set_fontsize( 8 )
for tick in ax2.yaxis.get_major_ticks():
    tick.label.set_fontsize( 8 )

ax2.set_yscale('log')
ax2.set_xscale('log')
ax2.set_xlabel( r"$t$" , fontsize=8 )
ax2.set_ylabel( r"Loshmidt Echo" , fontsize=8 )
ax2.tick_params(labelsize=6)
ax2.yaxis.set_ticks(np.linspace(0.000001,0.01,2))
ax2.xaxis.set_ticks(np.linspace(10,1000,2))
ax2.set_xlim( ( 10 , 1000 ) )
ax2.xaxis.set_label_coords(0.5, -0.025)
ax2.yaxis.set_label_coords(-0.05, 0.5)

fig.savefig( figname, bbox_inches = 'tight' )

