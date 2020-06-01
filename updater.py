import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import math

path = './server/'

urlConfirmed = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
urlDeaths = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
urlCountries = 'https://restcountries.eu/rest/v2/all'
urlCovidData = 'https://covid.ourworldindata.org/data/owid-covid-data.json'
super_file = 'super_file.csv'
#urlTemp = 'https://crudata.uea.ac.uk/cru/data/hrg/cru_ts_3.23/crucy.1506241137.v3.23/countries/tmp/crucy.v3.23.1901.2014.{}.tmp.per'
wldMean = 773


df_cc = pd.read_csv(urlConfirmed)
indexesConfirmed = np.arange(2, len(df_cc.columns) - 1)
df_cc.drop(df_cc.columns[indexesConfirmed], axis=1, inplace=True)
df_cc.drop(df_cc.columns[0], axis=1, inplace=True)
df_cc.columns = ['Name','Cases']
dict_cc = {"Name": [], "Cases": []}

name = df_cc.iloc[0,0]
count = 0

for i in range(0, len(df_cc.index)-1):
    n = df_cc.iloc[i,0]
    if not n == name:
    	if name in dict_cc["Name"]:
    		dict_cc["Cases"][dict_cc["Name"].index(name)] += count
    	else:
	    	dict_cc["Name"].append(name)
	    	dict_cc["Cases"].append(count)
    	name = df_cc.iloc[i, 0]
    	if name == 'US':
    		name = 'United States of America'
    	count = 0
    count += df_cc.iloc[i, 1]

df_cc = pd.DataFrame.from_dict(dict_cc)


df_de = pd.read_csv(urlDeaths)
indexesDeaths = np.arange(2, len(df_de.columns) - 1)
df_de.drop(df_de.columns[indexesDeaths], axis=1, inplace=True)
df_de.drop(df_de.columns[0], axis=1, inplace=True)
df_de.columns = ['Name', 'Deaths']

dict_de = {"Name": [], "Deaths": []}

name = df_de.iloc[0,0]
count = 0

for i in range(0, len(df_de.index)-1):
    n = df_de.iloc[i,0]
    if not n == name:
    	if name in df_de["Name"]:
    		dict_de["Deaths"][dict_de["Name"].index(name)] += count
    	else:
	    	dict_de["Name"].append(name)
	    	dict_de["Deaths"].append(count)
    	name = df_de.iloc[i,0]
    	if name == 'US':
    		name = 'United States of America'
    	count = 0
    count += df_de.iloc[i, 1]

df_de = pd.DataFrame.from_dict(dict_de)
df_de.drop(df_de.columns[0], axis=1, inplace=True)



r = requests.get(urlCountries)
arrCountries = r.json()
names = []
populations = []
areas = []
dds = []
lats = []
longs = []
codes = []

for country in arrCountries:
    name = country["name"]
    population = country["population"]
    area = country["area"]
    latlng = country["latlng"]
    code = country["alpha3Code"]
    
    if name == None or population == None or area == None or latlng == None or code == None:
        continue
        
    names.append(name)
    populations.append(population)
    areas.append(area)
    dds.append((population/area))
    lats.append(latlng[0])
    longs.append(latlng[1])
    codes.append(code)
    
dictCountries = {"Name": names, "Code": codes, "Latitude":lats, "Longitude":longs, "Population": populations, "Area": areas, "Demographic_Density": dds}
df_co = pd.DataFrame.from_dict(dictCountries)



df_super = pd.read_csv(super_file)
dict_super = {"Code": []}
code = df_super.iloc[0, 1]
dict_super["Code"].append(code)

for l in range(0, len(df_super.index)):
    series_name = df_super.iloc[l, 2]
    if not code == df_super.iloc[l, 1]:
        code = df_super.iloc[l, 1]
        
        if not str(code) == 'nan':
            dict_super["Code"].append(code)
        
    if not isinstance(series_name, str) or not isinstance(code, str):
        continue
    
    
    for c in range(len(df_super.columns)-1, -1, -1):
        value = df_super.iloc[l, c]
        if (isinstance(value, int) and math.isnan(value)):
            continue
        try:
            value = float(value)
        except:
            value = df_super.iloc[l, c]
            if not value == '..':
                if series_name in dict_super:
                    dict_super[series_name].append(np.nan)
                else:
                    dict_super[series_name] = [np.nan]
                break
            continue

        if series_name in dict_super:
            dict_super[series_name].append(value)
        else:
            dict_super[series_name] = [value]
            
        break

df_super = pd.DataFrame.from_dict(dict_super)
arr = ['Population ages 65 and above (% of total population)', 'Urban population (% of total population)', 'Demographic Density', 'Hospital beds (per 1,000 people)', 'Code']
df_super.drop(df_super.loc[:, ~df_super.columns.isin(arr)], axis=1, inplace=True)
#df_super.drop(['Investment in water and sanitation with private participation (current US$)', 'Community health workers (per 1,000 people)', 'Adequacy of social safety net programs (% of total welfare of beneficiary households)', 'Adequacy of social insurance programs (% of total welfare of beneficiary households)', 'Railways, passengers carried (million passenger-km)', 'Completeness of death registration with cause-of-death information (%)', 'Population in urban agglomerations of more than 1 million (% of total population)', 'Electric power consumption (kWh per capita)', 'Smoking prevalence, total (ages 15+)' ,'Average precipitation in depth (mm per year)'], axis=1, inplace=True)
df_super.drop([len(df_super.index)-1], inplace=True)



r = requests.get(urlCovidData)
dict_json_cpm = r.json()
dict_cpm = {"Code": [], "Cases_per_mil": []}
for key in dict_json_cpm.keys():
    cpm = dict_json_cpm[key][len(dict_json_cpm[key])-1]
    try:
        cpm = cpm['total_cases_per_million']
    except:
        cpm = cpm['total_cases']/(cpm['population']/10**6)
    dict_cpm["Code"].append(key)
    if cpm > wldMean:
        dict_cpm["Cases_per_mil"].append('Above')
    else:
        dict_cpm["Cases_per_mil"].append('Below')
df_cpm = pd.DataFrame.from_dict(dict_cpm)




df_final = df_cc
df_final['Deaths'] = df_de['Deaths']
df_final['Cases_per_mil'] = df_cpm['Cases_per_mil']
df_final = df_final.join(df_co.set_index('Name'), on='Name')
df_final = df_final.join(df_super.set_index('Code'), on='Code')
df_final.set_index('Name', inplace=True)


df_final = df_final.dropna()

df_final.to_csv(path+'final.csv')