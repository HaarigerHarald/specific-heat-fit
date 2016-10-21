import os
import re
import sys

import numpy as np
import matplotlib.pyplot as plt

import scipy.constants as cons
from scipy.optimize import curve_fit
from scipy import integrate

filepath = ""

fit1_upper_temperature = 3.1 # in Kelvin ... 0.0 = ignore
fit2_upper_temperature = 0.0 # in Kelvin ... 0.0 = ignore

Sample_HC_Unit = 1e-6 # for μJ


R = cons.R

if len(sys.argv) > 1:
    filepath = sys.argv[1]

print("File:", os.path.basename(filepath))
print("===========================================================")

masRegex = re.compile("INFO,((\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?),MASS:")
molWghtRegex = re.compile("INFO,((\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?),MOLWGHT:")
atomsRegex = re.compile("INFO,((\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?),ATOMS:")
masErrorRegex = re.compile("INFO,((\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?),MASSERR:")

mas = 0.0
molWght = 0.0
atomsPerUnit = 0.0
masError = 0.0

f = open(filepath)
skip = 0
dataTagFound = False
line = f.readline()
while line:
    mo = masRegex.search(line)
    if mo != None:
        mas = float(mo.group(1))
        
    mo = molWghtRegex.search(line)
    if mo != None:
        molWght = float(mo.group(1))
    
    mo = atomsRegex.search(line)
    if mo != None:
        atomsPerUnit = float(mo.group(1))
        
    mo = masErrorRegex.search(line)
    if mo != None:
        masError = float(mo.group(1))
    
    if line.startswith("[Data]"):
        dataTagFound = True
        break
    skip += 1
    line = f.readline()
f.close()

if not dataTagFound:
    skip = 0
else:
    skip += 2

if mas == 0.0:
    print("Sample mas not found in data file!")
    mas = float(input("Enter sample mas in mg: "))
    
if molWght == 0.0:
    print("Formula weight not found in data file!")
    molWght = float(input("Enter formula weight in g/mole: "))
    
if atomsPerUnit == 0.0:
    print("Atoms per formula unit not found in data file!")
    atomsPerUnit = float(input("Enter atoms per formula unit: "))


tdata, hcdata, hcerr = np.genfromtxt(filepath, skip_header=skip, delimiter=",", usecols=(6,8,9), unpack=True)

hcdata = (hcdata*Sample_HC_Unit)*molWght/(mas*1e-3)
hcerr = (hcerr*Sample_HC_Unit)*molWght/(mas*1e-3) + masError*hcdata/mas # not used

tdataCopy = tdata 
hcdataCopy = hcdata
hcerrCopy = hcerr

if fit1_upper_temperature > 0:   
    del_indices = []
    it = np.nditer(tdata , flags=['f_index'])
    while not it.finished:
        if it[0] > fit1_upper_temperature:
            del_indices.append(it.index)
        it.iternext()
    
    for index in reversed(del_indices):
        tdata  = np.delete(tdata , index)
        hcdata = np.delete(hcdata, index)
        hcerr = np.delete(hcerr, index)

def simple_func(T, a, b):
    return a*T + b*T**3
    
popt, pcov = curve_fit(simple_func, tdata, hcdata, p0=(0.01, 0.01), bounds=(0, np.inf))

a = popt[0] # \gamma
b = popt[1] # \beta

error = [] 
for i in range(len(popt)):
    try:
        error.append(np.absolute(pcov[i][i])**0.5)
    except:
        error.append(0.00)

residuals = hcdata - simple_func(tdata , a,b)
fres = sum(residuals**2)

print("Low Temperature fit from 0 -",fit1_upper_temperature, "K as: γ*T + β*T^3")
print("γ:", a, "±", error[0])
print("β:", b, "±", error[1])
print("-----------------------------------------------------------")
print("Squares of residuals:", fres)
print("===========================================================")
  
tdata  = tdataCopy
hcdata = hcdataCopy
hcerr = hcerrCopy

if fit2_upper_temperature > 0:   
    del_indices = []
    it = np.nditer(tdata , flags=['f_index'])
    while not it.finished:
        if it[0] > fit2_upper_temperature:
            del_indices.append(it.index)
        it.iternext()
    
    for index in reversed(del_indices):
        tdata  = np.delete(tdata , index)
        hcdata = np.delete(hcdata, index)
        hcerr = np.delete(hcerr, index)

    
def debyeIntegral(t, args):
    T, m, e, d = args
    return 9*R*(atomsPerUnit-(e+d)/(3*R))*((T/m)**3)*(t**4)*np.exp(t)/(np.exp(t)-1)**2

def func(T, m, c, d, e, g):
  return (a*T+ integrate.quad(debyeIntegral, 0, m/T, [T, m, e, d])[0]+d*((c/T)**2)*np.exp(c/T)/((np.exp(c/T)-1)**2)+e*((g/T)**2)*np.exp(g/T)/((np.exp(g/T)-1)**2))/T**3 

vfunc = np.vectorize(func, excluded=set([1]))

popt, pcov = curve_fit(vfunc, tdata , hcdata/tdata**3, p0=(242 , 28, 41, 181, 70), bounds=(0, np.inf))

m = popt[0] # Debye Temperature
c = popt[1] # Einstein Temperature 1
d = popt[2] # N Einstein 1
e = popt[3] # N Einsetein 2
g = popt[4] # Einstein Temperature 2

error = [] 
for i in range(len(popt)):
    try:
        error.append(np.absolute(pcov[i][i])**0.5)
    except:
        error.append(0.00)
   
residualsCubed = hcdataCopy/tdataCopy**3 - vfunc(tdataCopy, m, c, d, e, g)
fresCubed = sum(residualsCubed**2)

residuals = hcdataCopy - vfunc(tdataCopy, m, c, d, e, g)*(tdataCopy)**3
fres = sum(residuals**2)

if fit2_upper_temperature == 0.0:
    print("Fit with a Debye and 2 Einstein Modes")
else:
    print("Fit from 0 -", fit2_upper_temperature, "K with a Debye and 2 Einstein Modes")
    

print("N Debye:                ", (atomsPerUnit-(d+e)/(3*R)), "±", (error[2]/+error[3])/(3*R))
print("Debye Temperature:      ", m, "±", error[0] , "K")
print("N Einstein 1 :          ", d/(3*R),"±", error[2]/(3*R) )
print("Einstein 1 Temperature: ", c, "±", error[1] , "K")
print("N Einstein 2:           ", e/(3*R), "±", error[3]/(3*R))
print("Einstein 2 Temperature: ", g, "±", error[4] , "K")
print("------------------------------------------------------------")
print("Squares of residuals over T^3:", fresCubed)
print("Squares of residuals:         ", fres)

def debyeIntegrated(x):
    return integrate.quad(debyeIntegral, 0, m/x, [x, m, e ,d])[0]

vDebye = np.vectorize(debyeIntegrated, excluded=set([1]))

plt.clf()
plt.rcParams['mathtext.default'] = 'regular'
plt.plot(tdataCopy, hcdataCopy/tdataCopy**3, 'o', markersize=7)
plt.plot(tdataCopy, vfunc(tdataCopy ,m,c,d,e,g), linewidth=2.0)
plt.plot(tdataCopy, vDebye(tdataCopy)/tdataCopy**3, linewidth=2.0)
plt.plot(tdataCopy, (d*((c/tdataCopy)**2)*np.exp(c/tdataCopy)/((np.exp(c/tdataCopy)-1)**2))/tdataCopy**3, linewidth=2.0)
plt.plot(tdataCopy, (e*((g/tdataCopy)**2)*np.exp(g/tdataCopy)/((np.exp(g/tdataCopy)-1)**2))/tdataCopy**3, linewidth=2.0)
plt.xscale('log')
plt.ylabel('$C_p/T^3 [J/K^4/mole]$', fontsize=18)
plt.xlabel('T [K]', fontsize=18)
plt.grid(True, which='both')
plt.minorticks_on()
plt.show()
