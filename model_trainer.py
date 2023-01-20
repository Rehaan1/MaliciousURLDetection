import pandas as pd
import re
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn import metrics
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt


def reading_dataset():
    df = pd.read_csv('malicious_phish.csv')
    df = data_preprocessing(df)
    print(df.head())

def data_preprocessing(df: pd.DataFrame):

    # Changing Values to Malicious and Safe
    print("---------------------------------------")
    print("Processing to Change Values to Malicious and Safe ......")
    df = df.replace({'phishing': 'malicious'}, regex=True)
    df = df.replace({'defacement': 'malicious'}, regex=True)
    df = df.replace({'benign': 'safe'}, regex=True)
    df = df.replace({'malware': 'malicious'}, regex=True)
    
    # Removing Null Values if any
    print("---------------------------------------")
    print("Delete Null Value..............")
    df = df[pd.notnull(df['url'])]
    
    #Label Encode type
    print("---------------------------------------")
    print("Label Encoding Type..............")
    df['category_id'] = df['type'].factorize()[0]
    
    
    return df
    

reading_dataset()
