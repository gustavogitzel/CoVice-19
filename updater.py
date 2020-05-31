import requests
import json
import numpy as np
import pandas as pd

path = './data/'

urlConfirmed = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
urlDeaths = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
urlCountries = 'https://restcountries.eu/rest/v2/all'
urlTemp = 'https://crudata.uea.ac.uk/cru/data/hrg/cru_ts_3.23/crucy.1506241137.v3.23/countries/tmp/crucy.v3.23.1901.2014.{}.tmp.per'


def confirmed_cases():
	dfConfirmed_cases = pd.read_csv(urlConfirmed)
	indexesConfirmed = np.arange(2, len(dfConfirmed_cases.columns) - 1)
	dfConfirmed_cases.drop(dfConfirmed_cases.columns[indexesConfirmed], axis=1, inplace=True)
	dfConfirmed_cases.drop(dfConfirmed_cases.columns[0], axis=1, inplace=True)
	dfConfirmed_cases.rename(index={0: "country", 1: "cases"})
	dfConfirmed_cases.to_csv(path+'confirmed_cases.csv')
	print(dfConfirmed_cases)

def deaths():
	dfDeaths = pd.read_csv(urlDeaths)
	indexesDeaths = np.arange(2, len(dfDeaths.columns) - 1)
	dfDeaths.drop(dfDeaths.columns[indexesDeaths], axis=1, inplace=True)
	dfDeaths.drop(dfDeaths.columns[0], axis=1, inplace=True)
	dfDeaths.rename(index={0: "country", 1: "deaths"})
	dfDeaths.to_csv(path+'deaths.csv')

def population():
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
	dictCountries = {"name": names, "code": codes, "latitude":lats, "longitude":longs, "population": population, "area": areas, "demographic_density": dds}
	dfCountries = pd.DataFrame.from_dict(dictCountries)
	dfCountries.to_csv(path+'countries.csv')

	#for i in range(0, len(names)):
		#name = names[i]
		#lat = lats[i]
		#r = requests.get(urlTemp.format(name))
		#print(r.text)

def air_quality():
	pass

def icus():
	pass

confirmed_cases()
deaths()
population()
air_quality()
icus()