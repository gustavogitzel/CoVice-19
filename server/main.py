from flask import Flask, redirect, url_for, render_template, flash, json, jsonify, request
import pandas as pd
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/")
def home():
    return "Teste"


@app.route("/submit", methods=['POST'])
@cross_origin()
def submit():
    density = request.form['density']
    air = request.form['air']
    icu = request.form['icu']
    isolation = request.form['isolation']

    # chamar algoritmo pedro
    return "teste submit" # retorna json pro site 
    
@app.route('/country/<name>', methods=['GET'])
@cross_origin()
def country(name):
	df = pd.read_csv('final.csv')
	df.set_index('Name', inplace=True)
	df.drop(df.columns[0], axis=1, inplace=True)
	return df.loc[name].to_json()

if __name__ == "__main__":
    app.run()

