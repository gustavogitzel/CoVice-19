from flask import Flask, redirect, url_for, render_template, flash, json, jsonify, request

app = Flask(__name__)

@app.route("/")
def home():
    return "Teste"

@app.route("/submit", methods=['POST'])
def submit():
    density = request.form['density']
    air = request.form['air']
    icu = request.form['icu']
    isolation = request.form['isolation']

    # chamar algoritmo pedro
    return "teste submit" # retorna json pro site 
    

if __name__ == "__main__":
    app.run()

