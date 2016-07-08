'''
This code gathers from two files containing information on the consumption levels
of alcohol by state, and the states GSP.

It then creates a attempts to find correlations between the data, through a variety
of different methods.

By: Tyler Sullivan

'''

import csv
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

# this section maps and labels the data to a displayed graph
def datamap(fdata, titleappend):
    # runs data through pandas crosstab function
    print("\n============================================================\n")
    ctab = pd.crosstab(fdata['Consumption'] > fdata['Consumption'].mean(), fdata['GSP'] > fdata['GSP'].mean())
    plt.figure()
    matplotlib.style.use("ggplot")
    plt.plot(fdata['GSP'], [fdata['Consumption'].mean() for num in fdata['Consumption']], label="Consumption Mean", linestyle = '--')
    plt.plot([fdata['GSP'].mean() for num in fdata['GSP']], fdata['Consumption'], label="GSP Mean", linestyle = '--')
    plt.scatter(fdata['GSP'], fdata['Consumption'], label="States")
    plt.title('Alcohol Consumption' + titleappend + ' vs GSP')
    plt.ylabel('Consumption (per million)')
    plt.xlabel('GSP (per thousand)')
    plt.legend(loc = "lower right")
    plt.savefig("plot" + titleappend + ".png")
    plt.show()
    print(ctab)

# opens raw data files and parses necessary information into pandas data structures
# first try with sum of volume totals
try:
    with open("niaaa-report.csv") as alcoholfile:
        rd = csv.reader(alcoholfile)
        adata = pd.DataFrame([[float(row[2]), float(row[3]), float(row[4])] for row in rd if row[1] == '2009'], columns=list('BWS'))
except:
    print("Error reading niaaa-report.csv")
adata_sum = pd.Series(adata.sum(axis=1), name = "Consumption")

# try volume weighted by alcohol content
adata_w = pd.DataFrame(adata)
adata_w['B'] = adata_w['B'] * 0.04
adata_w['W'] = adata_w['W'] * 0.14
adata_w['S'] = adata_w['S'] * 0.4
adata_w_sum = pd.Series(adata_w.sum(axis=1), name = "Consumption")

# try volume per type of alcohol
bdata = pd.Series(adata['B'], name="Consumption")
wdata = pd.Series(adata['W'], name="Consumption")
ldata = pd.Series(adata['S'], name="Consumption")

# gathers information regarding state GSP
try:
    with open("usgs_state_2009.csv") as spendingfile:
        rd = csv.reader(spendingfile)
        sdata = pd.Series([(float(row[5].replace(',','')) * 10**9) / (float(row[9]) * 10**6) / 1000 for row in rd if len(row) > 1 and 'All' not in row[0] and 'State' not in row[0]], name = 'GSP')
except:
    print("Error reading usgs_state_2009.csv")

# joins data sets together
fdata_w = pd.concat([adata_w_sum, sdata], axis=1)   # weighted data
fdata_beer = pd.concat([bdata, sdata], axis=1)      # just beer
fdata_wine = pd.concat([wdata, sdata], axis=1)      # just wine
fdata_spirits = pd.concat([ldata, sdata], axis=1)    # just liquor
fdata = pd.concat([adata_sum, sdata], axis=1)       # strictly by volume

# sets up graphing for each method
datamap(fdata, '(all by Volume)')
datamap(fdata_w, '(all by Alochol Content)')
datamap(fdata_beer, '(Beer)')
datamap(fdata_wine, '(Wine)')
datamap(fdata_spirits, '(Spirits)')
