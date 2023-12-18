import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_json('/Users/spencer/Desktop/CS-458-Fall-2023/Amazon Final Project/json/amazon-meta.json')
included_groups = ['Book', 'Music', 'Video', 'DVD']
filtered_df = df[df['group'].isin(included_groups)]
group_counts = filtered_df['group'].value_counts()

# Plot the data
group_counts.plot(kind='bar')
plt.title('Amazon Co-Purchasing Data: Total Items by Group')
plt.xlabel('Group')
plt.ylabel('Number of Items')
plt.xticks(rotation=45)  
plt.show()

