import requests
import json
import numpy as np
import pandas as pd

path = './data/'

urlConfirmed = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
urlDeaths = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
urlCountries = 'https://restcountries.eu/rest/v2/all'


def confirmed_cases():
	dfConfirmed_cases = pd.read_csv(urlConfirmed)
	indexesConfirmed = np.arange(4, len(dfConfirmed_cases.columns) - 1)
	dfConfirmed_cases.drop(dfConfirmed_cases.columns[indexesConfirmed], axis=1, inplace=True)
	dfConfirmed_cases.to_csv(path+'confirmed_cases.csv')

def deaths():
	dfDeaths = pd.read_csv(urlDeaths)
	indexesDeaths = np.arange(4, len(dfDeaths.columns) - 1)
	dfDeaths.drop(dfDeaths.columns[indexesDeaths], axis=1, inplace=True)
	dfDeaths.to_csv(path+'deaths.csv')

def population():
	r = requests.get(urlCountries)
	arrCountries = r.json()
	names = []
	populations = []
	areas = []
	dds = []
	for country in arrCountries:
		name = country["name"]
		population = country["population"]
		area = country["area"]
		if name == None or population == None or area == None:
			continue
		names.append(name)
		populations.append(population)
		areas.append(area)
		dds.append((population/area))
	dictCountries = {"name": names, "population": population, "area": areas, "demographic_density": dds}
	dfCountries = pd.DataFrame.from_dict(dictCountries)
	dfCountries.to_csv(path+'countries.csv')

confirmed_cases()
deaths()
population()