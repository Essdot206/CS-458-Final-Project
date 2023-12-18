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
videos_df = df[df['group'] == 'Video'].copy()
asin_to_title = pd.Series(videos_df.title.values, index=videos_df.ASIN).to_dict()


def replace_asin_with_title(similar_list):
    if isinstance(similar_list, list) and len(similar_list) > 1:
        return [asin_to_title.get(asin, asin) for asin in similar_list[1:]]
    return []


videos_df.loc[:, 'similar_titles'] = videos_df['similar'].apply(replace_asin_with_title)
videos_info = pd.DataFrame()
videos_info['title'] = videos_df['title']
videos_info['similar'] = videos_df['similar_titles'].apply(lambda x: ', '.join(x))
videos_info[['num_ratings', 'avg_rating']] = videos_df.apply(
    lambda row: extract_review_info(row['reviews']),
    axis=1, result_type='expand'
)

output_dir = '/Users/spencer/Desktop/CS-458-Fall-2023/Amazon Final Project/Excel'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
top_videos = videos_info.sort_values(by=['avg_rating', 'num_ratings'], ascending=[False, False]).head(50)
print(top_videos)
top_videos.to_excel('/Users/spencer/Desktop/CS-458-Fall-2023/Amazon Final Project/Excel/top_videos.xlsx', index=False)
