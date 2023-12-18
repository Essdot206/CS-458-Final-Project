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
dvds_df = df[df['group'] == 'DVD'].copy()
asin_to_title = pd.Series(dvds_df.title.values, index=dvds_df.ASIN).to_dict()


def replace_asin_with_title(similar_list):
    if isinstance(similar_list, list) and len(similar_list) > 1:
        return [asin_to_title.get(asin, asin) for asin in similar_list[1:]]
    return []


dvds_df.loc[:, 'similar_titles'] = dvds_df['similar'].apply(replace_asin_with_title)
dvds_info = pd.DataFrame()
dvds_info['title'] = dvds_df['title']
dvds_info['similar'] = dvds_df['similar_titles'].apply(lambda x: ', '.join(x))
dvds_info[['num_ratings', 'avg_rating']] = dvds_df.apply(
    lambda row: extract_review_info(row['reviews']),
    axis=1, result_type='expand'
)

output_dir = '/Users/spencer/Desktop/CS-458-Fall-2023/Amazon Final Project/Excel'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
top_dvds = dvds_info.sort_values(by=['avg_rating', 'num_ratings'], ascending=[False, False]).head(50)
print(top_dvds)
top_dvds.to_excel('/Users/spencer/Desktop/CS-458-Fall-2023/Amazon Final Project/Excel/top_dvds.xlsx', index=False)
