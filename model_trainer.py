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
    print(df.head)

reading_dataset()
