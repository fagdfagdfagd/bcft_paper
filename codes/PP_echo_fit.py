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

bc = 'PP' 
path = "../data/" + bc + "/"
fig_path = "../images/"
figname = fig_path + bc +"_fit.pdf"

offset=0.15/25*pi/2/pi

dataset = []
for (dirpath, dirnames, filenames) in walk(path):
    dataset.extend(filenames)

for filename in dataset:
    if filename[0]=='.':
        dataset.remove( filename )
# print( dataset ) 

# ----------------------------------------------------------------------           
#                         error bar and slope                          |           
# ----------------------------------------------------------------------
def fit_data( x, y ,where ):
    
    log_x = np.log( x ) / np.log( 10 )
    log_y = np.log( y ) / np.log( 10 )

    if where=='left_center':
        print( x )
        print( 'left_center' )
        log_x = log_x[ (x>1000)*(x<2000) ]
        log_y = log_y[ (x>1000)*(x<2000) ]        
    elif where=='right_center':
        print( x )
        print( 'right_center' )
        log_x = log_x[ (x>400)*(x<2000) ]
        log_y = log_y[ (x>400)*(x<2000) ] 
    elif where=='right':
        # print( 'right' )
        log_x = log_x[ (x>100)*(x<300) ]
        log_y = log_y[ (x>100)*(x<300) ]
    else:
        log_x = log_x[ (x>100)*(x<1000) ]
        log_y = log_y[ (x>100)*(x<1000) ]
    slope, _, _, _, std_err = scipy.stats.linregress( log_x, log_y )

    error = std_err

    return -slope, error 

slope = []
error = []
x = []

for filename in dataset:
   if filename[0]=='.':
       continue
   # extract x = theta / pi from filename
   x.append( float( filename.split('_')[1] ) )

# print x
# print slope    
# print error

# sort index
x = np.array( x )
idx = np.argsort( x )
x = x[idx]

dataset = np.array( dataset )
# print( dataset )
dataset = dataset[idx]
# print( dataset )

for filename in dataset:
   data = np.loadtxt( path + filename )
   t = data[:,0]
   echo = data[:,1]
   if filename in dataset[18:24]:
        where='left_center'
   elif filename in dataset[28:33]:
        where='right_center'
   elif filename in dataset[37:51]:
        where='right'
   else:
        where='others'
   print( filename )
   this_slope, this_error = fit_data( t, echo , where );
   slope.append( this_slope )
   error.append( this_error )


inset_data = np.loadtxt( path + dataset[4] )
t_inset = inset_data[:,0]
echo_inset = inset_data[:,1]
inset_data = np.loadtxt( path + dataset[8] )
t_inset_2 = inset_data[:,0]
echo_inset_2 = inset_data[:,1]
inset_data = np.loadtxt( path + dataset[18] )
t_inset_3 = inset_data[:,0]
echo_inset_3 = inset_data[:,1]


# ---------------------------------------------------------------------- 
#                           plot and insets                            |
# ---------------------------------------------------------------------- 

fig, ax = plt.subplots( 1, 1, squeeze = True, figsize = ( 4.5, 3 ) )

x_analy = np.linspace( 0 , 0.5 , 200 )
x_analy = [this_x_analy-offset  for this_x_analy in x_analy]

y_analy = (-1)*2 * ( np.square([this_x_analy-0.25 for this_x_analy in x_analy]) - [abs(this_x_analy-0.25) for this_x_analy in x_analy] ) 

# y_analy = (-1)*2 * ( np.square(x_analy-0.25) - abs(x_analy-0.25) ) 
ax.plot( x_analy , y_analy , c = 'red' , label = r"analytical $2\left(\left|\frac{\theta}{\pi} - \frac{1}{4}\right| - \left(\frac{\theta}{\pi} - \frac{1}{4} \right)^2\right)$" )
# ax.plot( x , [-this_slope for this_slope in slope] , 'o', markersize = 2, c = 'black', markeredgewidth=0.0 , label = "numerical" )

# numerical results
(_, caps, _) = ax.errorbar( x, slope, yerr = error, fmt='o', color = 'black', capsize = 1, markersize = 2, label = "numerical" ) 
for cap in caps:
    cap.set_markeredgewidth( 1 )

# inset position
left, bottom, width, height = [0.4, 0.42, 0.25, 0.25]
ax2 = fig.add_axes([left, bottom, width, height])
ax2.plot( t_inset, echo_inset , 'o' , markersize = 1.5  , c = colorL[6] , label = r"$\theta=0.02\pi$" )
ax2.plot( t_inset_2, echo_inset_2 , 'o' , markersize = 1.5 , c = colorL[8] , label = r"$\theta=0.12\pi$" )
ax2.plot( t_inset_3, echo_inset_3 , 'o' , markersize = 1.5 , c = colorL[10] , label = r"$\theta=0.24\pi$" )
# plt.text(0.05, 0.95,'(a)', ha='center', va='center', transform=ax.transAxes)

# ----------------------------------------------------------------------           
#                         title label and axis                         |           
# ----------------------------------------------------------------------

ax.set_xlim( ( 0, 0.5 ) )
ax.set_ylim( ( 0 , 0.6 ) ) 

ax.set_xlabel( r"$\frac{\theta}{\pi}$" , fontsize=15 )
ax.set_ylabel( r"Echo Exponent" )
# ax.errorbar( x , slope , yerr=error , fmt='k.')
  
ax.legend( loc = 'upper left', frameon = False, prop = {'size':10}, ncol=1, handlelength=3 )

# smaller font for inset
for tick in ax2.xaxis.get_major_ticks():
    tick.label.set_fontsize( 8 )
for tick in ax2.yaxis.get_major_ticks():
    tick.label.set_fontsize( 8 )

ax2.set_yscale('log')
ax2.set_xscale('log')
ax2.set_xlabel( r"$t$" , fontsize=8 )
ax2.set_ylabel( r"Echo" , fontsize=8 )
# ax2.tick_params(labelsize=6)
ax2.yaxis.set_ticks(np.linspace(0.001,0.1,2))
# ax2.xaxis.set_ticks(np.linspace(10,1000,2))
ax2.set_xlim( ( 10 , 1000 ) )
# ax2.xaxis.set_label_coords(0.5, -0.025)
ax2.yaxis.set_label_coords(-0.05, 0.5)

fig.savefig( figname, bbox_inches = 'tight' )

