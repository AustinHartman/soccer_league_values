#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 13:02:05 2018

@author: austinhartman
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# argument represents csv of values of individual clubs season by season
df  = pd.read_csv("seriea_club_values.csv")

# change the formatting of the club value data to cast to float
df['total value'] = df[df.columns[3]].replace('[\£m]', '', regex=True).astype(float)


sns.lmplot('year', 'total value', data=df, hue='club', fit_reg=False)

df.dtypes

# take the sum of each club from each season and put in series x 
x = df.groupby('year')['total value'].sum()


plt.plot(x)

# change title according to league
plt.title("Serie A total value growth")
plt.ylabel("Millions of pounds")
plt.xlabel("year")
