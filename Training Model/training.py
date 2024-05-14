import pandas as pd 
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression, RidgeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score
import pickle

from sklearn.linear_model import LogisticRegression


# Initialize Logistic Regression model with a higher max_iter value and a different solver
model = LogisticRegression(max_iter=70000, solver='sag')  # Adjust max_iter and solver as needed


# Load data
df = pd.read_csv('coords.csv')

# Exclude non-numeric columns from X
X = df.drop('class', axis=1)

# Convert the remaining columns to a NumPy array
X_array = X.to_numpy()

# Define target variable
y = df['class']

# Split data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X_array, y, test_size=0.3, random_state=1234)

# Define classification pipelines
pipelines = {
    'lr': make_pipeline(StandardScaler(), LogisticRegression()),
    'rc': make_pipeline(StandardScaler(), RidgeClassifier()),
    'rf': make_pipeline(StandardScaler(), RandomForestClassifier()),
    'gb': make_pipeline(StandardScaler(), GradientBoostingClassifier()),
}

# Fit models
fit_models = {}
for algo, pipeline in pipelines.items():
    model = pipeline.fit(X_train, y_train)
    fit_models[algo] = model

# Evaluate models
for algo, model in fit_models.items():
    accuracy = model.score(X_test, y_test)
    print(f"{algo}: Accuracy = {accuracy:.2f}")

for algo, model in fit_models.items():
    yhat = model.predict (X_test)
    print (algo, accuracy_score(y_test, yhat))

fit_models['rf'].predict(X_test)

with open('body_language.pkl', 'wb') as f:
    pickle.dump(fit_models['rf'],f)