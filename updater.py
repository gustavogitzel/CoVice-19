import requests
import json
import numpy as np
import pandas as pd

path = './data/'

urlConfirmed = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
urlDeaths = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'


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
	r = requests.get('https://www.worldpop.org/rest/data/pop/pic?iso3=bra')
	print(json.dumps(r.json(), indent=2, sort_keys=True))


population()