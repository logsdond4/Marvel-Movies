# -*- coding: utf-8 -*-
"""
Author: Dan Logsdon
Date: 10/12/2020

Description: This code analyzes the top 10 movies for the past 20 years.


"""

#%% Import Packages
import pandas as pd
import os

#%% Data Import
root = os.path.dirname(os.path.dirname(__file__)) #root folder
src = root + '\\src' #source folder
file = src + '\\Top 10 Movies per Year.csv' #movie data
key = src + '\\Consumer Price Index.csv' #consumer price index for adjusted

df=pd.read_csv(file) #input movie data
cpi=pd.read_csv(key) #input CPI key

#%% Globals
cpi_dict=pd.Series(cpi.CPI.values,index=cpi.Year).to_dict() #create dictionary

#%% Functions
def data_flag(df): #creates and cleans up flags
    df.loc[df['marvel_flag'] == 1, 'studio_flag'] = 'Marvel'
    df.loc[((df['domestic_distributor'] == 'Walt Disney ') & (df['marvel_flag'] == 0)), 'studio_flag'] = 'Disney'
    df.loc[((df['domestic_distributor'] != 'Walt Disney ') & (df['marvel_flag'] == 0)), 'studio_flag'] = 'Other'
    return df

def CPI_calc(df, cpi_dict): #adjust revenue for inflation
    df['CPI']=df['release_year'].map(cpi_dict)
    df['CPI_ratio']=df.CPI[0]/df.CPI
    
    df['domestic_adj']=df.domestic_gross*df.CPI_ratio
    df['budget_adj']=df.film_budget*df.CPI_ratio
    df['worldwide_adj']=df.worldwide_gross*df.CPI_ratio
    return df

#%% Clean Data
df=data_flag(df)

#%% Calculate Adjusted Revenue
df=CPI_calc(df, cpi_dict)

#%% Data Export
root = os.path.dirname(os.path.dirname(__file__)) #root folder
path = root + '\\Output' #Output folder
file = path + '\\Top 10 Movies per Year_cleaned.csv' #consumer price index for adjusted
df.to_csv(file)

