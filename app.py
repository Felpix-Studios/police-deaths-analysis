import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os, sys, random, pickle
import calmap

pd.set_option("display.max_rows", None, "display.max_columns", None)

data=pd.read_excel('MPVDatasetDownload.xlsx',index_col=0)

font = {'family': 'sans-serif','weight': 'normal','size': 8}

plt.rc('font', **font)

# Set up charts
plt.style.use('seaborn')
fig, axs = plt.subplots(4,2)
fig.tight_layout(pad=1.0)
cmap = plt.get_cmap('Spectral')
colors = [cmap(i) for i in np.linspace(0, 1, 8)]
stateColors = [cmap(i) for i in np.linspace(0, 1, 51)]

# Titles

axs[0,0].set_title("Killings by Race Against Population per Million")
axs[1,0].set_title("Killings by State")
axs[2,0].set_title("Killings by Gender")
axs[3,0].set_title("Killings over Time")
axs[3,1].set_title("Killings during 2020")
axs[0,1].set_title("Killings by Day")
axs[1,1].set_title("Killings by Race")
axs[2,1].set_title("Killings by Accountability")
print(data.head())

# Get race related data
race_labels = data["Victim's race"].value_counts().index
race_counts = data["Victim's race"].value_counts()

# Make the charts
axs[1,1].pie(race_counts,labels=race_labels,autopct="%1.1f%%",colors=colors)

# Select White, Black, and Latino
proprace_counts = race_counts[0:3].astype(float)

# Population numbers bellow gathered from 2019 Census demographic estimations
proprace_counts[0] = proprace_counts[0]/250446756.0
proprace_counts[1] = proprace_counts[1]/43984096.0
proprace_counts[2] = proprace_counts[2]/60724312.0

proprace_counts = proprace_counts.sort_values(ascending=False)

print(proprace_counts)
print(proprace_counts.index)

axs[0,0].bar(proprace_counts.index,proprace_counts, color=colors)

# Get state data
state_labels = data["State"].value_counts().index
state_counts = data["State"].value_counts()

axs[1,0].bar(state_labels,state_counts,color=stateColors)

# Gender data
gender_labels = data["Victim's gender"].value_counts().index
gender_counts = data["Victim's gender"].value_counts()
gender_percents= []
total = float(sum(gender_counts))

for x in range(len(gender_counts)):
    gender_percents.append(gender_counts[x]/total)

axs[2,0].bar(gender_labels,gender_percents)

# Y/Y data
time_count = data["Date of Incident (month/day/year)"].groupby(data["Date of Incident (month/day/year)"].dt.year).agg('count')

time_count=time_count[0:-1]

axs[3,0].plot(time_count, color="red")

# D/D data
day_data = data["Date of Incident (month/day/year)"].groupby(data["Date of Incident (month/day/year)"]).agg('count')
day_data.rolling(30,center=True)
day_dates = data["Date of Incident (month/day/year)"].value_counts().index
day_count = data["Date of Incident (month/day/year)"]

print(day_count)

axs[0,1].plot(day_data)
calmap.yearplot(day_data,daylabels='MTWTFSS',year=2020,ax=axs[3,1])

#day_count.drop()

# Drop unknown category
#data.drop(data[data["Criminal Charges?"] == "No known charges"].index, inplace = True)

# Reframe data for simplification
data.loc[data["Criminal Charges?"] == "Charged, Acquitted", "Criminal Charges?"] = "No"
data.loc[data["Criminal Charges?"] == "Charged, Mistrial", "Criminal Charges?"] = "No"
data.loc[data["Criminal Charges?"] == "NO", "Criminal Charges?"] = "No"
data.loc[data["Criminal Charges?"] == "Charged with a crime, Acquitted", "Criminal Charges?"] = "No"
data.loc[data["Criminal Charges?"] == "Charged, Charges Tossed", "Criminal Charges?"] = "No"
data.loc[data["Criminal Charges?"] == "Charged, Charges Dropped", "Criminal Charges?"] = "No"
data.loc[data["Criminal Charges?"] == "Charged, Convicted, Sentenced to 30 years in prison", "Criminal Charges?"] = "Charged, Convicted"
data.loc[data["Criminal Charges?"] == "Charged, Convicted, Sentenced to 20 years in prison", "Criminal Charges?"] = "Charged, Convicted"
data.loc[data["Criminal Charges?"] == "Charged, Convicted, Sentenced to 5 years in prison", "Criminal Charges?"] = "Charged, Convicted"
data.loc[data["Criminal Charges?"] == "Charged, Convicted, Sentenced to 50 years", "Criminal Charges?"] = "Charged, Convicted"
data.loc[data["Criminal Charges?"] == "Charged, Convicted, Sentenced to 40 years in prison", "Criminal Charges?"] = "Charged, Convicted"
data.loc[data["Criminal Charges?"] == "Charged, Convicted, Sentenced to 1 year in jail, 3 years suspended", "Criminal Charges?"] = "Charged, Convicted"
data.loc[data["Criminal Charges?"] == "Charged, Convicted, Sentenced to 1 year in prison", "Criminal Charges?"] = "Charged, Convicted"
data.loc[data["Criminal Charges?"] == "Charged, Convicted, Sentenced to 2.5 years in prison", "Criminal Charges?"] = "Charged, Convicted"
data.loc[data["Criminal Charges?"] == "Charged, Convicted, Sentenced to 6 years", "Criminal Charges?"] = "Charged, Convicted"
data.loc[data["Criminal Charges?"] == "Charged, Convicted, Sentenced to 18 months", "Criminal Charges?"] = "Charged, Convicted"
data.loc[data["Criminal Charges?"] == "Charged, Convicted, Sentenced to 5 years probation.", "Criminal Charges?"] = "Charged, Convicted"
data.loc[data["Criminal Charges?"] == "Charged, Convicted, Sentenced to life in prison", "Criminal Charges?"] = "Charged, Convicted"
data.loc[data["Criminal Charges?"] == "Charged, Convicted, Sentenced to Life in Prison.", "Criminal Charges?"] = "Charged, Convicted"
data.loc[data["Criminal Charges?"] == "Charged, Convicted, Sentenced to Life in Prison", "Criminal Charges?"] = "Charged, Convicted"
data.loc[data["Criminal Charges?"] == "Charged with manslaughter", "Criminal Charges?"] = "Charged with a crime"
data.loc[data["Criminal Charges?"] == "Charged, Mistrial, Plead Guilty to Civil Rights Charges", "Criminal Charges?"] = "Charged, Convicted"
data.loc[data["Criminal Charges?"] == "Charged, Convicted, Sentenced to 3 months in jail", "Criminal Charges?"] = "Charged, Convicted"
data.loc[data["Criminal Charges?"] == "Charged, Convicted, Sentenced to 6 years in prison", "Criminal Charges?"] = "Charged, Convicted"
data.loc[data["Criminal Charges?"] == "Charged, Convicted, Sentenced to 16 years in prison", "Criminal Charges?"] = "Charged, Convicted"
data.loc[data["Criminal Charges?"] == "Charged, Convicted, Sentenced to 40 years to Life in prison", "Criminal Charges?"] = "Charged, Convicted"
data.loc[data["Criminal Charges?"] == "Charged, Convicted, Sentenced to 25 years in prison", "Criminal Charges?"] = "Charged, Convicted"
data.loc[data["Criminal Charges?"] == "Charged, Convicted, Sentenced to 40 years in prison", "Criminal Charges?"] = "Charged, Convicted"
data.loc[data["Criminal Charges?"] == "Charged, Convicted, Sentenced to 3 years probation", "Criminal Charges?"] = "Charged, Convicted"
data.loc[data["Criminal Charges?"] == "Charged, Convicted, Sentenced to 4 years", "Criminal Charges?"] = "Charged, Convicted"
data.loc[data["Criminal Charges?"] == "Charged, Convicted, Sentenced to life in prison without parole, plus 16 years", "Criminal Charges?"] = "Charged, Convicted"

data.loc[data["Criminal Charges?"] == "Charged with a crime", "Criminal Charges?"] = "Charged"
data.loc[data["Criminal Charges?"] == "No", "Criminal Charges?"] = "Not Charged"


#print(data["Criminal Charges?"])
#print(data["Criminal Charges?"].count())
account_labels = data["Criminal Charges?"].value_counts().index
account_counts = data["Criminal Charges?"].value_counts()
#axs[2,1].pie(account_counts,labels=account_labels,autopct="%1.1f%%",colors=colors)
axs[2,1].bar(account_labels,account_counts,color=colors)

plt.show()