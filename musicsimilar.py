import pandas as pd
import re
import os

def extract_review_info(reviews_str):
    num_ratings_match = re.search(r'total: (\d+)', reviews_str)
    avg_rating_match = re.search(r'avg rating: (\d)', reviews_str)    
    num_ratings = int(num_ratings_match.group(1)) if num_ratings_match else 0
    avg_rating = int(avg_rating_match.group(1)) if avg_rating_match else 0
    
    return num_ratings, avg_rating

df = pd.read_json('/Users/spencer/Desktop/CS-458-Fall-2023/Amazon Final Project/json/amazon-meta.json')
musics_df = df[df['group'] == 'Music'].copy()
asin_to_title = pd.Series(musics_df.title.values, index=musics_df.ASIN).to_dict()


def replace_asin_with_title(similar_list):
    if isinstance(similar_list, list) and len(similar_list) > 1:
        return [asin_to_title.get(asin, asin) for asin in similar_list[1:]]
    return []


musics_df.loc[:, 'similar_titles'] = musics_df['similar'].apply(replace_asin_with_title)
musics_info = pd.DataFrame()
musics_info['title'] = musics_df['title']
musics_info['similar'] = musics_df['similar_titles'].apply(lambda x: ', '.join(x))
musics_info[['num_ratings', 'avg_rating']] = musics_df.apply(
    lambda row: extract_review_info(row['reviews']),
    axis=1, result_type='expand'
)

output_dir = '/Users/spencer/Desktop/CS-458-Fall-2023/Amazon Final Project/Excel'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
top_musics = musics_info.sort_values(by=['avg_rating', 'num_ratings'], ascending=[False, False]).head(50)
print(top_musics)
top_musics.to_excel('/Users/spencer/Desktop/CS-458-Fall-2023/Amazon Final Project/Excel/top_musics.xlsx', index=False)
