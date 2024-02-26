# This script is written to do a rock-property analysis to Well B 
# by estimating p-wave velocity, s-wave velocity, Vp over Vs ratio,  
# acoustic impedance and poission's ratio

import numpy as np 
import matplotlib.pyplot as plt

# import csv file that has Well B data
Data = np.genfromtxt('well_B.csv', delimiter=',', skip_header=1)

depth = Data[:, 0]  #depth in feet
rho_log = Data[:, 3]  #measured density log
sonic_log = Data[:, 4]   #measured sonic log 

# import csv file that has petrophysical well logs
petrophysical = np.genfromtxt('petrophysical.csv', delimiter=',', skip_header=1)
V_shale = petrophysical[:, 0]  #volume of shale
V_sand = petrophysical[:, 1]   #volume of sand

def primary_velocity(sonic_log):
    '''This function is used to estimate the p-wave velocity'''
    p_velocity = (1e6*0.0003048)/sonic_log
    return (p_velocity)

def shear_velocity(p_velocity, V_shale, V_sand):
    '''This function is used to estimate the s-wave velocity using 
           Greenberg-Castagna equation'''
    s_velocity1 = 1/((V_sand/(0.80416*p_velocity -0.85588)) + (V_shale/
                   (0.76969*p_velocity -0.86735 ))) 
    s_velocity2 = (V_sand*(0.80416*p_velocity -0.85588)) + (V_shale*
                   (0.76969*p_velocity -0.86735 ))
    s_velocity = (s_velocity1+s_velocity2)/2
    return (s_velocity)

def Acoustic(p_velocity, rho):
    '''This function is used to estimate the acoustic impedance'''
    acoustic_impedance = p_velocity*rho
    return (acoustic_impedance)

def velocity_ratio(p_velocity, s_velocity):
    '''This function is used to estimate the p-wave over s-wave velocity ratio'''
    VpOverVs = p_velocity/s_velocity
    return (VpOverVs)

def poission (VpOverVs):
    '''This function is used to estimate the poission ratio'''
    poission_ratio =  (0.5 - ((1/VpOverVs)**2)) / (1 - ((1/VpOverVs)**2))
    return (poission_ratio)

#estimate the p-wave velocity
p_velocity = primary_velocity(sonic_log)
#estimate the s-wave velocity
s_velocity = shear_velocity(p_velocity, V_shale, V_sand)
#estimate the Vp/Vs ratio
VpOverVs = velocity_ratio(p_velocity, s_velocity)
#estimate the poission's ratio
poission_ratio = poission (VpOverVs)

#Density log editing 
for i in range (0, len (rho_log)):
    if rho_log[i] >=2.65:
       rho_log[i]=2.65
    else : 
       rho_log[i]=rho_log[i]

#estimate the acoustic impedance
acoustic_impedance = Acoustic(p_velocity, rho_log)

#create three tracks for the well logs
fig, ax = plt.subplots(1, 3, figsize=(12, 14))
fig.set_facecolor('violet')

#plotting acoustic impedance
ax[0].plot(acoustic_impedance  , depth, 'red')
ax[0].grid()
ax[0].set_xlabel( 'AI', fontsize = 16)
ax[0].set_ylabel( 'Depth (Feet)', fontsize = 16)
ax[0].set_xlim(8 , 11)
ax[0].set_ylim(5100, 5450)
ax[0].invert_yaxis()
ax[0].axhline(y = 5210, xmin = 0, xmax = 1, color = 'black', lw = 2.5, 
              linestyle='dashed', alpha = 0.8)
ax[0].axhline(y = 5340, xmin = 0, xmax = 1, color = 'black', lw = 2.5, 
              linestyle='dashed', alpha = 0.8)

#plotting Vp/Vs ratio
ax[1].plot(VpOverVs  , depth, 'blue')
ax[1].grid()
ax[1].set_xlabel( 'Vp/Vs', fontsize = 16)
ax[1].set_xlim(1.6 , 1.9)
ax[1].set_ylim(5100, 5450)
ax[1].invert_yaxis()
ax[1].axhline(y = 5210, xmin = 0, xmax = 1, color = 'black', lw = 2.5, 
              linestyle='dashed', alpha = 0.8)
ax[1].axhline(y = 5340, xmin = 0, xmax = 1, color = 'black', lw = 2.5, 
              linestyle='dashed', alpha = 0.8)

#plotting poission's ratio
ax[2].plot(poission_ratio , depth, 'green')
ax[2].grid()
ax[2].set_xlabel( 'Poission ratio', fontsize = 16)
ax[2].set_xlim(0.2 , 0.3)
ax[2].set_ylim(5100, 5450)
ax[2].invert_yaxis()
ax[2].axhline(y = 5210, xmin = 0, xmax = 1, color = 'black', lw = 2.5, 
              linestyle='dashed', alpha = 0.8)
ax[2].axhline(y = 5340, xmin = 0, xmax = 1, color = 'black', lw = 2.5, 
              linestyle='dashed', alpha = 0.8)

# list the results 
result= np.array((p_velocity,s_velocity, rho_log, VpOverVs, 
                  poission_ratio, acoustic_impedance))
result=result.T

# Save the results to csv file
np.savetxt('rockphysics.csv', result, delimiter=','
            , header='p_velocity,s_velocity, rho_log, VpOverVs,' 
                      'poission_ratio, acoustic_impedance')