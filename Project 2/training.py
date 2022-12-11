import pandas as pd
import numpy as np

# Load the data into a pandas DataFrame
df = pd.read_json("heroes.json")
# df = df.transpose()

# Use the get_dummies function to perform one-hot encoding
df_encoded = pd.get_dummies(df, columns=['name'])

# Print the resulting DataFrame
for column in df_encoded:
    for index, row in df_encoded.iterrows():
        print(f"{row[column]:>3}", end=" ")
    print(column)
