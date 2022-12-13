"""import pandas as pd
import numpy as np
#from sklearn.model_selection import train_test_split
#from sklearn.neural_network import MLPClassifier
import csv
import time

st = time.time()

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


print(time.time() - st)"""
import pickle
import numpy as np
import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split

# Load the data from the CSV file
# df = pd.read_csv("sortedDataGameMode22.csv", header=None)
df = pd.read_csv("duoDataDire.csv", header=None)

df = df.values
X = df[:, :2]
y = df[:, 2]
# for i in range(0, 10):
#     if X is None:
#         X = df[:1000, i:1 + i]
#         y = df[:1000, 10]
#     elif i < 5:
#         X = np.vstack((X, df[:1000, i:1 + i]))
#         y = np.hstack((y, df[:1000, 10]))
#     else:
#         X = np.vstack((X, df[:1000, i:1 + i] + 130))
#         y = np.hstack((y, df[:1000, 10]))


# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Define the network architecture
mlp = MLPClassifier(hidden_layer_sizes=(128, 128), max_iter=1500, activation='relu', solver='sgd', verbose=True, tol=1e-4, random_state=100, learning_rate_init=.01)

# Train the model
mlp.fit(X_train, y_train)

# Evaluate the model on the test data
accuracy = mlp.score(X_test, y_test)
print(accuracy)
pickle.dump(mlp, open('finalized_model1.sav', 'wb'))

for i in range(0, 100):
    # if mlp.predict([X_test[i]]) == y_test[i]:
    #     print(y_test[i], X_test[i], end=" ")
    #     print("Correct")
    print(i, mlp.predict([[i, i+10]]))


# mlp = pickle.load(open('finalized_model.sav', 'rb'))
# result = mlp.score(X_test, y_test)
# print(result)
