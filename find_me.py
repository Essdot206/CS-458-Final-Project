import pandas as pd

def find_items(group, category, num_items=5):
    df = pd.read_json('/Users/spencer/Desktop/CS-458-Fall-2023/Amazon Final Project/json/amazon-meta.json')
    filtered_df = df[df['group'] == group]

    # Check if 'categories' column exists and is a string before applying 'contains'
    if 'categories' in df.columns and category:
        filtered_df = filtered_df[filtered_df['categories'].astype(str).str.contains(category)]

    item_titles = filtered_df['title'].head(num_items).tolist()
    return item_titles

if __name__ == "__main__":
    group = input("Enter the group (e.g., Book, DVD, Music, Video): ")
    category = input("Enter the category (leave empty if not applicable): ")
    items = find_items(group, category)
    print("What we found for you:")
    for item in items:
        print(item)

