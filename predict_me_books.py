import pandas as pd
import os
import re
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

def load_and_prepare_data(filepath):
    df = pd.read_json(filepath)
    df = df[df['group'] == 'Book']
    df['num_ratings'], df['avg_rating'] = zip(*df['reviews'].map(extract_review_info))
    df['num_similar'] = df['similar'].apply(lambda x: len(x) - 1 if isinstance(x, list) else 0)
    
    return df

def extract_review_info(reviews_str):
    num_ratings_match = re.search(r'total: (\d+)', reviews_str)
    avg_rating_match = re.search(r'avg rating: (\d)', reviews_str)    
    num_ratings = int(num_ratings_match.group(1)) if num_ratings_match else 0
    avg_rating = int(avg_rating_match.group(1)) if avg_rating_match else 0
    
    return num_ratings, avg_rating

def predict_sales_rank(df):
    X = df[['num_ratings', 'avg_rating', 'num_similar']]
    y = df['salesrank']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    df['predicted_salesrank'] = model.predict(X)

    return df


def find_top_books(df, n=10):
    top_books = df.sort_values(by='predicted_salesrank').head(n)
    return top_books[['title', 'predicted_salesrank']]


def replace_asin_with_title(similar_list, asin_to_title):
    if isinstance(similar_list, list) and len(similar_list) > 1:
        return [asin_to_title.get(asin, asin) for asin in similar_list[1:]]
    return []

if __name__ == "__main__":
    books_df = load_and_prepare_data('/Users/spencer/Desktop/CS-458-Fall-2023/Amazon Final Project/json/amazon-meta.json')
    asin_to_title = pd.Series(books_df.title.values, index=books_df.ASIN).to_dict()
    books_df['similar_titles'] = books_df['similar'].apply(lambda x: replace_asin_with_title(x, asin_to_title))
    books_df = predict_sales_rank(books_df)
    top_books = find_top_books(books_df)

    output_dir = '/Users/spencer/Desktop/CS-458-Fall-2023/Amazon Final Project/Excel'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    print("Top Predicted Books:")
    print(top_books)
    top_books.to_excel('/Users/spencer/Desktop/CS-458-Fall-2023/Amazon Final Project/Excel/predicted_books.xlsx', index=False)
