# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 15:05:42 2020

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
hmat3 = []
matx = np.zeros((19, 25))
countec = np.zeros((19, 25))
matx3 = np.zeros((24, 3))
countec3 = np.zeros((24,3))

for f_name in sorted(glob.glob('frm_tec_ddr_*.csv')):
    print(f_name)
    data = pd.read_csv(f_name)
    tst = data['LOCAL_TRUE_SOLAR_TIME'][0:].values
    lat = data['LATITUDE'][0:].values
    tec = data['TEC'][0:].values

    gtst = np.arange(0, 25, 1)
    glat = np.arange(-90, 100, 10)
    mat = np.zeros((19, 25))
    mat3 = np.zeros((24, 3))

    for p in range(len(glat)-1):
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
            
            mat[p][i] = (0 if len(idx) == 0 else np.mean(tec[idx]))
            if mat[p][i] != 0:
                countec[p][i] += 1
            
            if p < 3:
                mat3[i][p] = (0 if len(idx) == 0 else np.mean(tec[idx]))
                if mat3[i][p] != 0:
                    countec3[i][p] += 1
    
    hmat.append(mat)
    hmat3.append(mat3)

for b in range(len(hmat)):
    matx = np.sum( np.array([ matx, hmat[b] ]), axis=0 )

for b3 in range(len(hmat)):
    matx3 = np.sum( np.array([ matx3, hmat3[b3] ]), axis=0 )
    
countec[countec == 0] = 'nan'
matx = np.divide(matx, countec)
#matx[np.isnan(matx)] = 0

countec3[countec3 == 0] = 'nan'
matx3 = np.divide(matx3, countec3)
matx3[np.isnan(matx3)] = 0

matxx3 = np.zeros((24, 1))
countecx3 = np.zeros((24, 1))
for m in range(len(matx3)):
    for n in range(len(matx3[m])):
        matxx3[m][0] = matxx3[m][0] + matx3[m][n]
        if matx3[m][n] != 0:
            countecx3[m][0] += 1

countecx3[countecx3 == 0] = 'nan'
matxx3 = np.divide(matxx3, countecx3)

fig = plt.figure(figsize = (9, 10))
gs = gridspec.GridSpec(4, 5)

ax1 = fig.add_subplot(gs[0:2, :])
img = ax1.pcolor(gtst, glat, matx)
cbar = plt.colorbar(img)
plt.title('(Grid Data)')
plt.yticks(np.arange(-90, 110, 20))
plt.xlabel('LOCAL TRUE SOLAR TIME \n (decimal hours)')
plt.ylabel('LATITUDE \n(degree)')
cbar.set_label('TOTAL ELECTRON CONTENT (TEC) \n (electrons per squared meters)')

ax2 = fig.add_subplot(gs[2:4,:-1])
gtstx3 = np.arange(0, 24, 1)
plt.title('Total Electron Content (TEC) variation with LOCAL TRUE SOLAR TIME', fontsize = 10)
ax2.plot(gtstx3, matxx3, 'b')
ax2.plot(gtstx3, matxx3, 'o')
plt.ylabel('TOTAL ELECTRON CONTENT (TEC) \n (electrons per squared meters)')
plt.xlabel('LOCAL TRUE SOLAR TIME \n (degree)')

plt.subplots_adjust(hspace = 1)
plt.show()
plt.savefig('figplott9', bbox_inches = 'tight')
