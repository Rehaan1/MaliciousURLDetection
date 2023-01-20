import pandas as pd
import re
from joblib import Parallel, delayed
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn import metrics
from sklearn.metrics import classification_report
from urllib.parse import urlparse


def reading_dataset():
    df = pd.read_csv('malicious_phish.csv')
    df = data_preprocessing(df)
    df = attribute_extraction(df)
    print(df.head())
    random_forest_model_generator(df)

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
    
    # Label Encode type
    print("---------------------------------------")
    print("Label Encoding Type..............")
    df['category_id'] = df['type'].factorize()[0]

    return df

def attribute_extraction(df: pd.DataFrame):
    
    print("---------------------------------------")
    print("Attribute Extraction in Process..............")

    # Count number of dots
    df['count .'] = df['url'].apply(lambda i: i.count('.'))

    # Count number of digits
    df['digits_count'] = df['url'].apply(lambda i: digit_count(i))

    # Count number of letters
    df['letters_count']=df['url'].apply(lambda i: letter_count(i))

    # Count number of special characters
    df['special_count']=df['url'].apply(lambda i: special_char_count(i))

    # URL Length
    df['url_length'] = df['url'].apply(lambda i: len(i))
    
    # Digits to Char Ratio
    df['digits_to_char_ratio'] = df['url'].apply(lambda i : digit_to_char_ratio(i))

    # Check for HTTP
    df['has_http'] = df['url'].apply(lambda i: 1 if 'http:' in i else 0)

    # URL Based Checks
    df['path_length'] = df['url'].apply(lambda i: len(urlparse(i).path))
    df['host_length'] = df['url'].apply(lambda i: len(urlparse(i).netloc))
    df['no_of_fragments'] = df['url'].apply(lambda i: len(urlparse(i).fragment) )
    df['no_of_subdomain'] = df['url'].apply(lambda i: len(i.split('http')[-1].split('//')[-1].split('/')[0].split('.')) - 1)
    df['num_uppercase'] = df['url'].str.count(r'[A-Z]')
    df['num_lowercase'] = df['url'].str.count(r'[a-z]')
    df['upper_lower_ratio'] = df['num_uppercase'] / (df['num_lowercase']+1)
    df['num_param'] = df['url'].apply(lambda i: i.split("?")[-1].count('='))

    return df

def random_forest_model_generator(df: pd.DataFrame):

    print("---------------------------------------")
    print("Generating Random Forest Model..............")

    X=df.drop(columns=['url','type','category_id'])
    y=df['category_id']

    print("---------------------------------------")
    print("Creating Pipeline..............")

    rfc_pipeline = Pipeline([('scaler',StandardScaler()), ('RandomForest',RandomForestClassifier(n_estimators=50))])

    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.33)
    
    print("---------------------------------------")
    print("Fitting Train Data..............")

    rfc_pipeline.fit(X_train,y_train)

    print("---------------------------------------")
    print("Predicting Test Data..............")

    y_pred = rfc_pipeline.predict(X_test)

    print("---------------------------------------")
    print("Report of Model Generated..............")

    report=classification_report(y_pred=y_pred, y_true=y_test)
    print("Random Forest Classification Report")
    print(report)

    print("---------------------------------------")
    print("Saving Model..............")

    # Save the model as a pickle in a file
    joblib.dump(rfc_pipeline, 'maliciousURLModelRandom.pkl')


    #Uncomment the following only to test generated model
    #testing_generated_model(X_test, y_test)

def testing_generated_model(X_test, y_test):
    
    print("---------------------------------------")
    print("Testing generated Model..............")

    model_from_joblib = joblib.load('maliciousURLModelRandom.pkl')
    y_pred = model_from_joblib.predict(X_test)
    
    report=classification_report(y_pred=y_pred, y_true=y_test)
    print("---------------------------------------")
    print("Loaded Model Random Forest Classification Report......")
    print(report)

def digit_count(string):
    digit=0
    all_digits = ['0', '1', '2', '3', '4',
              '5', '6', '7', '8', '9']
    for i in string:
        if (i in all_digits):
            digit+=1
    return digit

def letter_count(string):
    letter=0
    for i in string:
        if (i.isalpha()):
            letter+=1
    return letter

def special_char_count(string):
    special=0
    all_special = ['@', '!', '#', '$', '%',
              '^', '&', '*', '-', '+', '=', '?']
    for i in string:
        if (i in all_special):
            special+=1
    return special
    
def digit_to_char_ratio(string):
    letter=0
    for i in string:
        if (i.isalpha()):
            letter+=1
    digit=0
    all_digits = ['0', '1', '2', '3', '4',
              '5', '6', '7', '8', '9']
    for i in string:
        if (i in all_digits):
            digit+=1
    if(letter==0):
        letter = 1
    digit_to_char_ratio = digit/letter
    return digit_to_char_ratio
    

reading_dataset()
