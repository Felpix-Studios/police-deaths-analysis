import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os, sys, random, pickle

sns.set(style="darkgrid")

data=pd.read_excel('MPVDatasetDownload.xlsx',index_col=0)

# Set up charts
fig, axs = plt.subplots(2)
cmap = plt.get_cmap('Spectral')
colors = [cmap(i) for i in np.linspace(0, 1, 8)]

#Titles
axs[0].set_title("Race of Those Killed by Police")
axs[1].set_title("Killings by State")

print(data.head())

# Get race related data
race_labels = data["Victim's race"].value_counts().index
race_counts = data["Victim's race"].value_counts()

# Make the charts
race_pie = axs[0].pie(race_counts,labels=race_labels,autopct="%1.1f%%",colors=colors)

# Get state data
state_labels = data["State"].value_counts().index
state_counts = data["State"].value_counts()

state_pie = axs[1].pie(state_counts,labels=state_labels,autopct="%1.1f%%",colors=colors)

plt.show()