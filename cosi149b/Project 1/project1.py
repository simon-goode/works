import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import mean_squared_error
import csv

# read training data from the Excel sheet   
train_data = pd.read_csv('data_training.csv')

# separate features from target variable
X = train_data.drop('Label', axis=1)
y = train_data['Label']

# split data into training and testing sets
#       test_size=0.7 was chosen because it is generally good practice to leave 20-30% of your data available for testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.75, random_state=42)

# separate features into continuous and categorical features
continuous_features = ['Feature_1', 'Feature_3', 'Feature_8', 'Feature_9', 'Feature_10',
                       'Feature_11', 'Feature_12', 'Feature_13', 'Feature_14', 'Feature_15', 'Feature_16', 'Feature_17',
                       'Feature_18', 'Feature_19']
categorical_features = ['Feature_2', 'Feature_4', 'Feature_5', 'Feature_6', 'Feature_7']

# create a processing pipeline
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), continuous_features),
        ('cat', OneHotEncoder(), categorical_features)
    ])

# create a classification model
classifier = RandomForestClassifier(n_estimators=100)

# create a pipeline between the preprocessor and the model
pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', classifier)
])

# fit the model to training data
pipeline.fit(X_train, y_train)

# make predictions on the test set
#y_pred = pipeline.predict(X_test)
# mse = mean_squared_error(y_test, y_pred)
# print(f"MSE: {mse}")

# read sample data for prediction
sample_data = pd.read_csv('data_test.csv')

# make predictions on sample data
sample_predictions = pipeline.predict(sample_data)

# enumerate sample predictions into indexed rows
predictions_with_index = list(enumerate(sample_predictions, start=1))

# write predictions into output csv file
with open("P1_test_output.csv", mode='w', newline='') as file:
    writer = csv.writer(file)

    # write each prediction to file
    for _, prediction in predictions_with_index:
        writer.writerow([prediction])
print(f"predictions saved to P1_test_output.csv")