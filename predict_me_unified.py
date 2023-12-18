import pandas as pd
import os
import re
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import numpy as np

def load_and_prepare_data(filepath, category):
    df = pd.read_json(filepath)
    df = df[df['group'] == category]
    df['num_ratings'], df['avg_rating'] = zip(*df['reviews'].map(extract_review_info))
    df['num_similar'] = df['similar'].apply(lambda x: len(x) - 1 if isinstance(x, list) else 0)
    return df

def extract_review_info(reviews_str):
    num_ratings_match = re.search(r'total: (\d+)', reviews_str)
    avg_rating_match = re.search(r'avg rating: (\d)', reviews_str)    
    num_ratings = int(num_ratings_match.group(1)) if num_ratings_match else 0
    avg_rating = int(avg_rating_match.group(1)) if avg_rating_match else 0
    
    return num_ratings, avg_rating

def train_predict_model(df):
    X = df[['num_ratings', 'avg_rating', 'num_similar']]
    y = df['salesrank']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    print(f"RMSE: {rmse}")
    df['predicted_salesrank'] = model.predict(X)
    return df

def get_top_books(filepath):
    df = load_and_prepare_data(filepath, 'Book')
    top_books = df.sort_values(by=['avg_rating', 'num_ratings'], ascending=[False, False]).head(5)
    return top_books[['title', 'avg_rating', 'num_ratings']].to_dict(orient='records')


def predict_book_choice(filepath):
    df = load_and_prepare_data(filepath, 'Book')
    df = train_predict_model(df)
    return df[['title', 'predicted_salesrank']]

# Functions for DVDs
def get_top_dvds(filepath):
    df = load_and_prepare_data(filepath, 'DVD')
    top_dvds = df.sort_values(by=['avg_rating', 'num_ratings'], ascending=[False, False]).head(5)
    return top_dvds[['title', 'avg_rating', 'num_ratings']].to_dict(orient='records')

def predict_dvd_choice(filepath):
    df = load_and_prepare_data(filepath, 'DVD')
    df = train_predict_model(df)
    return df[['title', 'predicted_salesrank']]

# Functions for Music
def get_top_musics(filepath):
    df = load_and_prepare_data(filepath, 'Music')
    top_musics = df.sort_values(by=['avg_rating', 'num_ratings'], ascending=[False, False]).head(5)
    return top_musics[['title', 'avg_rating', 'num_ratings']].to_dict(orient='records')

def predict_music_choice(filepath):
    df = load_and_prepare_data(filepath, 'Music')
    df = train_predict_model(df)
    return df[['title', 'predicted_salesrank']]

# Functions for Videos
def get_top_videos(filepath):
    df = load_and_prepare_data(filepath, 'Video')
    top_videos = df.sort_values(by=['avg_rating', 'num_ratings'], ascending=[False, False]).head(5)
    return top_videos[['title', 'avg_rating', 'num_ratings']].to_dict(orient='records')

def predict_video_choice(filepath):
    df = load_and_prepare_data(filepath, 'Video')
    df = train_predict_model(df)
    return df[['title', 'predicted_salesrank']]


