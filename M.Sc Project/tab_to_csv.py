# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 14:51:48 2020

@author: HP
"""

import os
import pandas as pd

os.chdir(r'F:/TEC/')
for filename in os.listdir('F:/TEC/'):
    if filename.endswith(".tab"):
        print(filename)

        with open(filename, "r") as in_text:
            in_reade = pd.read_csv(in_text, sep='\s+', names = ['PULSE_NUMBER',	'EPHEMERIS_TIME', 'LATITUDE', 'LONGITUDE', 'LOCAL_TRUE_SOLAR_TIME', 'X_SC_MSO',	'Y_SC_MSO', 'Z_SC_MSO', 'SZA', 'TEC', 'A1	', 'A2',	'A3', 'FLAG'])
            
        file_name = os.path.splitext(filename)[0]
        with open(file_name + ".csv", "w", newline='') as f:
            in_reade.to_csv(f, index = False)
            print(file_name)