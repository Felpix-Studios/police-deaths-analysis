import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os, sys, random, pickle

data=pd.read_excel('MPVDatasetDownload.xlsx',index_col=0)

# Set up charts
fig, axs = plt.subplots(4,4)
cmap = plt.get_cmap('Spectral')
colors = [cmap(i) for i in np.linspace(0, 1, 8)]

# Titles
axs[0,0].set_title("Killings by Race")
axs[0,1].set_title("Killings by State")
axs[0,2].set_title("Killings by Gender")
axs[0,3].set_title("Killings over Time")
axs[1,0].set_title("Killings by Race Against Population per Million")
axs[1,1].set_title("Killings by Day")

print(data.head())

# Get race related data
race_labels = data["Victim's race"].value_counts().index
race_counts = data["Victim's race"].value_counts()

# Make the charts
axs[0,0].pie(race_counts,labels=race_labels,autopct="%1.1f%%",colors=colors)

# Select White, Black, and Latino
proprace_counts = race_counts[0:3].astype(float)

# Population numbers bellow gathered from 2019 Census demographic estimations
proprace_counts[0] = proprace_counts[0]/250446756.0*100000
proprace_counts[1] = proprace_counts[1]/43984096.0*100000
proprace_counts[2] = proprace_counts[2]/60724312.0*100000

proprace_counts = proprace_counts.sort_values(ascending=False)

print(proprace_counts)
print(proprace_counts.index)

axs[1,0].bar(proprace_counts.index,proprace_counts)

# Get state data
state_labels = data["State"].value_counts().index
state_counts = data["State"].value_counts()

axs[0,1].pie(state_counts,labels=state_labels,autopct="%1.1f%%",colors=colors)

# Gender data
gender_labels = data["Victim's gender"].value_counts().index
gender_counts = data["Victim's gender"].value_counts()
gender_percents= []
total = float(sum(gender_counts))

for x in range(len(gender_counts)):
    gender_percents.append(gender_counts[x]/total)

axs[0,2].bar(gender_labels,gender_percents)

# Y/Y data
time_count = data["Date of Incident (month/day/year)"].groupby(data["Date of Incident (month/day/year)"].dt.year).agg('count')

time_count=time_count[0:-1]

axs[0,3].plot(time_count)

# D/D data
day_count = data["Date of Incident (month/day/year)"].groupby(data["Date of Incident (month/day/year)"]).agg('count')

print(day_count)
print(day_count.index)
print(day_count.values)

axs[1,1].plot(day_count)

day_count.drop()

print(day_count)
plt.show()