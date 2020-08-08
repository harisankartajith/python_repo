# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 15:00:00 2020

@author: HP
"""

import os, glob
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import itertools
from matplotlib import gridspec

os.chdir(r'F:/TEC/')
hmat = []
hmat5 = []
matx = np.zeros((19, 19))
countec = np.zeros((19, 19))
matx5 = np.zeros((18, 3))
countec5 = np.zeros((18,3))

for f_name in sorted(glob.glob('frm_tec_ddr_*.csv')):
    print(f_name)
    data = pd.read_csv(f_name)
    sza = data['SZA'][0:].values
    lat = data['LATITUDE'][0:].values
    tec = data['TEC'][0:].values

    gsza = np.arange(0, 190, 10)
    glat = np.arange(-90, 100, 10)
    mat = np.zeros((19, 19))
    mat5 = np.zeros((18, 3))
    
    for p in range(len(glat)-1):
        hidx = []
        for q in range (len(lat)):
            if ((lat[q] >= glat[p]) & (lat[q] < glat[p+1])):
                hidx.append(q)
                
        for i in range(len(gsza)-1):
            vidx = []
            for j in range(len(sza)):
                if ((sza[j] >= gsza[i]) & (sza[j] < gsza[i+1])):
                    vidx.append(j)
            
            idx = []        
            for a in list(itertools.product(hidx, vidx)):
                if a[0] == a[1]:
                    idx.append(a[0])
            
            mat[p][i] = (0 if len(idx) == 0 else np.mean(tec[idx]))
            if mat[p][i] != 0:
                countec[p][i] += 1
                
            if p >= 6 and p <= 8:
                mat5[i][p-6] = (0 if len(idx) == 0 else np.mean(tec[idx]))
                if mat5[i][p-6] != 0:
                    countec5[i][p-6] += 1
                
    hmat.append(mat)
    hmat5.append(mat5)

for b in range(len(hmat)):
    matx = np.sum( np.array([ matx, hmat[b] ]), axis=0 )
    
for b5 in range(len(hmat5)):
    matx5 = np.sum( np.array([ matx5, hmat5[b5] ]), axis=0 )

countec[countec == 0] = 'nan'
matx = np.divide(matx, countec)
#matx[np.isnan(matx)] = 0

countec5[countec5 == 0] = 'nan'
matx5 = np.divide(matx5, countec5)
matx5[np.isnan(matx5)] = 0

matxx5 = np.zeros((18, 1))
countecx5 = np.zeros((18, 1))
for m in range(len(matx5)):
    for n in range(len(matx5[m])):
        matxx5[m][0] = matxx5[m][0] + matx5[m][n]
        if matx5[m][n] != 0:
            countecx5[m][0] += 1
            
countecx5[countecx5 == 0] = 'nan'
matxx5 = np.divide(matxx5, countecx5)

fig = plt.figure(figsize = (9, 10))
gs = gridspec.GridSpec(4, 5)

ax1 = fig.add_subplot(gs[0:2, :])
gszan = np.arange(0, 140, 10)
glatn = np.arange(-90, 100, 10)    
img = ax1.pcolor(gszan, glatn, np.delete(matx,[13,14,15,16,17,18],1))
cbar = plt.colorbar(img)
plt.title('(Grid Data)')
plt.yticks(np.arange(-90, 110, 20))
plt.xlabel('SOLAR ZENITH ANGLE (SZA) \n (degree)')
plt.ylabel('LATITUDE \n(degree)')
cbar.set_label('TOTAL ELECTRON CONTENT (TEC) \n (electrons per squared meters)')

ax2 = fig.add_subplot(gs[2:4, :-1])
gszax5 = np.arange(0, 180, 10)
plt.title('Total Electron Content (TEC) variation with SOLAR ZENITH ANGLE', fontsize = 10)
ax2.plot(gszax5, matxx5, 'b')
ax2.plot(gszax5, matxx5, 'o')
plt.ylabel('TOTAL ELECTRON CONTENT (TEC) \n (electrons per squared meters)')
plt.xlabel('SOLAR ZENITH ANGLE (SZA) \n (degree)')

plt.subplots_adjust(hspace = 1)
plt.show()
plt.savefig('figpltt8', bbox_inches = 'tight')
