import pandas as pd
import re
from joblib import Parallel, delayed
import joblib
from urllib.parse import urlparse

model = joblib.load('E:\VIT FILES\VIT Sem 6\Data  Mining\Project\Project\mlData\maliciousURLModelRandom.pkl')


def check_if_malicious(url):
    df = pd.DataFrame([url], columns=['url'])
    # Create and Extract Attributes from URL
    df = attribute_extraction(df)
    # print(df.head())
    df=df.drop(columns=['url'])
    
    # Predict if Malicious
    result = model.predict(df)
    if(result[0] == 0):
        print('{\"Decision\": \"Malicious\" }')
    else:
        print('{\"Decision\": \"Safe\" }')

def print_if_malicious(url):
    df = pd.DataFrame([url], columns=['url'])
    # Create and Extract Attributes from URL
    df = attribute_extraction(df)
    # print(df.head())
    df=df.drop(columns=['url'])
    
    print("---------------------------------------")
    print("*************Analysing URL Status**************")
    print("Please Wait..............")
    print()
    
    # Predict if Malicious
    result = model.predict(df)
    if(result[0] == 0):
        print("Decision: Malicious,")
    else:
        print("Decision: Safe")

def attribute_extraction(df: pd.DataFrame):
    
    #print("---------------------------------------")
    #print("Attribute Extraction in Process..............")

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

# Uncomment only for testing
# check_if_malicious("http://www.garage-pirenne.be/index.php?option=com_content&view=article&id=70&vsig70_0=15")
    