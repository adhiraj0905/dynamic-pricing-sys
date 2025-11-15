import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
import joblib # <-- The library for saving models
import os

print("--- Starting Model Training Script ---")

# --- 1. Load Data ---
# We assume the script is run from the root, so data is at './ride_sharing_data.csv'
try:
    data = pd.read_csv('ride_sharing_data.csv')
except FileNotFoundError:
    print("Error: 'ride_sharing_data.csv' not found. Make sure it's in the root folder.")
    exit()

print("Data loaded successfully.")

# --- 2. Define Features (X) and Target (y) ---
X = data.drop('Demand', axis=1)
y = data['Demand']

# --- 3. Define Preprocessing Steps ---
numerical_features = ['Price', 'Distance', 'Base_Price', 'Weather_Multiplier']
categorical_features = ['Time_of_Day', 'Weather']

all_features_in_data = list(X.columns)
numerical_features = [col for col in numerical_features if col in all_features_in_data]
categorical_features = [col for col in categorical_features if col in all_features_in_data]

numerical_transformer = Pipeline(steps=[('scaler', StandardScaler())])
categorical_transformer = Pipeline(steps=[('onehot', OneHotEncoder(handle_unknown='ignore'))])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer, numerical_features),
        ('cat', categorical_transformer, categorical_features)
    ],
    remainder='drop'
)

# --- 4. Train our FINAL Demand Model ---
final_model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', LinearRegression())
])

print("Training model on all data...")
final_model.fit(X, y)
print("Model training complete.")

# --- 5. Save the Model ---
# Create a 'models' directory if it doesn't exist
os.makedirs('models', exist_ok=True) 

# Save the model
model_path = 'models/demand_model_v1.joblib'
joblib.dump(final_model, model_path)

print(f"Model saved successfully to {model_path}")
print("--- Training Script Finished ---")