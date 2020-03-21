#%%
# Import Packages

import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import os
import numpy as np
import logging

pd.set_option('display.max_rows', 1000)
#%%
#Scrape AFl DFR Projections
URL = 'https://dailyfantasyrankings.com.au/resources/afl/2020/update/projections/satdsa2.htm'

df = pd.read_html(URL)[0]
df.columns = df.iloc[0,:]
df = df.iloc[2:,:]

df.to_csv('/Users/raymond.huynh/Desktop/python/Ray_Python/data/fantasy/afl_proj.csv', index=False)


# %%

#Data Cleaning
left = pd.read_csv('/Users/raymond.huynh/Desktop/python/Ray_Python/data/fantasy/ds_player_csv/ds_data.csv')
left.head()
left['Salary'] = left['Salary'] * 0.6

left[['First','Mid','Last']] = left.Name.str.split(expand=True) 

left['First_letter'] = left['First'].str[:1]

left["Last"].fillna("", inplace=True)
left["Player"] = left["First_letter"] + '.' + ' ' + left["Mid"] + left["Last"]



right = pd.read_csv('/Users/raymond.huynh/Desktop/python/Ray_Python/data/fantasy/afl_proj.csv') #Update FANDUEL File
columns = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11']
right.columns = ['1', 'Player', '3', '4', '5', '6', '7', '8', 'FPPG', '10', '11','12','13','14','15','16']
right.head()

result = pd.merge(right,left, how='left', on=['Player']) #.set_index('Player')
result.head(200)
cleaned_data = result.drop(['1','3', '4', '5', '6', '7', '8', '10', '11','12','13','14','15','16','Opponent','FPPG_y','Form','First','Mid','Last','First_letter'], axis=1)

cleaned_data.rename(columns = {'FPPG_x':'FPPG', 'Player ID':'ID', 'Playing Status':'Injury_Indicator'}, inplace = True) 

cleaned_data['Injury Indicator'] = cleaned_data.Injury_Indicator.str.replace("NAMED IN TEAM TO PLAY", " ").str.replace("INTERCHANGE", "").str.replace("NAMED AS EMERGENCY RESERVE","O")
cleaned_data = cleaned_data.drop(['Injury_Indicator'], axis=1).set_index('Player')
cleaned_data['FPPG'] = cleaned_data.FPPG.replace(np.NaN, '0')
cleaned_data['Salary'] = cleaned_data.Salary.replace(np.NaN, '0')
cleaned_data.head(100)
cleaned_data.to_csv('/Users/raymond.huynh/Desktop/python/Ray_Python/data/fantasy/cleaned_afl_ds_data.csv')


# %%
