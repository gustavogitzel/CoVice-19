import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.linear_model import LinearRegression

#Vars de controle
path = 'final.csv'
drop = [0, 1, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 22, 23, 24, 25, 26, 27, 28, 30, 31]
prever = [0, 1, -1] #Indices do novo DF!!

#Vars globais
normalizer = -1
df = -1
lm = -1

def inialize():
    global df
    global normalizer

    #Lendo
    df = pd.read_csv(path)

    #Arrumando colunas
    df.drop(df.columns[drop], axis=1, inplace=True)

    df_cases = df.iloc[:, 2]
    df.drop('Cases_per_mil', axis=1, inplace=True)

    cs = df.columns

    #Normalizando
    normalizer = preprocessing.Normalizer().fit(df)
    df = normalizer.transform(df)
    df = pd.DataFrame(df, columns = cs)

    df['Cases_per_mil'] = df_cases

    #Treinando
    lm = LinearRegression()
    lm.fit(df.iloc[2:, 2:-1], df.iloc[2:, 1])


def classify(dd, hb, pa, up):
    df_test = normalizer.transform([[dd, hb, pa, up]])
    df_test = pd.DataFrame(df_test)
    
    predict = lm0.predict(df_test)
    
    mudanca = 0
    menorDiferencaSegura = 9999
    menorDiferenca = 9999
    resulMaisProximo = 0
    
    for i in range(0, len(df.index)-1):
       
        dife = abs(df.iloc[i, 0] - predict[0])
        
        if df.iloc[i, -1] == 'Below' and dife < menorDiferencaSegura:
            menorDiferencaSegura = dife
            maiorSubDif = -1
            
            for ii in range(0, len(df.columns) - 3):
                subDif = abs(df.iloc[i, ii + 2] - df_test.iloc[0, ii])
                
                if subDif > maiorSubDif:
                    maiorSubDif = subDif
                    
                    if df.iloc[i, ii + 2] > df_test.iloc[0, ii]:
                        mudanca = -(ii + 1)
                    else:
                        mudanca = ii + 1
            
        if dife < menorDiferenca:
            menorDiferenca = dife
            resulMaisProximo = df.iloc[i, -1]
            
    return [resulMaisProximo, mudanca]