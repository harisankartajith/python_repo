# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 15:24:52 2020

@author: HP
"""

import os, glob
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import itertools
import matplotlib.patches as mpatches

os.chdir(r'F:/TEC/')
hmat = []
matx = np.zeros((25, 3))
countec = np.zeros((25,3))

for f_name in sorted(glob.glob('frm_tec_ddr_*.csv')):
    print(f_name)
    data = pd.read_csv(f_name)
    tst = data['LOCAL_TRUE_SOLAR_TIME'][0:].values
    lat = data['LATITUDE'][0:].values
    tec = data['TEC'][0:].values

    gtst = np.arange(0, 26, 1)
    glat = np.arange(-90, 110, 10)
    mat = np.zeros((25, 3))

    for p in range(3):
        hidx = []
        for q in range (len(lat)):
            if ((lat[q] >= glat[p]) & (lat[q] < glat[p+1])):
                hidx.append(q)
        
        for i in range(len(gtst)-1):
            vidx = []
            for j in range(len(tst)):
                if ((tst[j] >= gtst[i]) & (tst[j] < gtst[i+1])):
                    vidx.append(j)
            
            idx = []        
            for a in list(itertools.product(hidx, vidx)):
                if a[0] == a[1]:
                    idx.append(a[0])
            
            mat[i][p] = (0 if len(idx) == 0 else np.mean(tec[idx]))
            if mat[i][p] != 0:
                countec[i][p] += 1
                
    hmat.append(mat)

for b in range(len(hmat)):
    matx = np.sum( np.array([ matx, hmat[b] ]), axis=0 )

countec[countec == 0] = 'nan'
matx = np.divide(matx, countec)
matx[np.isnan(matx)] = 0

matxx = np.zeros((25, 1))
countecx = np.zeros((25, 1))
for m in range(len(matx)):
    for n in range(len(matx[m])):
        matxx[m][0] = matxx[m][0] + matx[m][n]
        if matx[m][n] != 0:
            countecx[m][0] += 1

countecx[countecx == 0] = 'nan'
matxx = np.divide(matxx, countecx)

tec1 = np.zeros((13, 1))
tec2 = np.zeros((13, 1))
for o in range(len(matxx)):
    if o <= 12:
        tec1[o][0] = matxx[o][0]
    if o >= 12:
        tec2[24-o][0] = matxx[o][0]        
 
gtec = np.arange(0, 13, 1)

plt.rcParams['xtick.bottom'] = True
plt.rcParams['xtick.top'] = True

plt.plot(gtec, tec2, 'r')
plt.plot(gtec, tec1, 'b')

red_patch = mpatches.Patch(color='red', label='The Dawn side')
blue_patch = mpatches.Patch(color = 'blue', label = 'The Dusk side')
plt.legend(handles=[blue_patch, red_patch])

plt.title('24             22             20             18             16             14             12\n', fontsize = 10)
plt.ylabel('TOTAL ELECTRON CONTENT (TEC) \n (electrons per squared meters)')
plt.xlabel('LOCAL TRUE SOLAR TIME \n (degree)', fontsize = 8)

plt.show()
plt.savefig('figpltt6', bbox_inches = 'tight')
