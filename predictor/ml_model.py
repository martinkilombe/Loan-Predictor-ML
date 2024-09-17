import joblib
from django.conf import settings
import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib
from django.conf import settings

model_path = os.path.join(settings.BASE_DIR, 'predictor', 'loan_predictor_model.joblib')
model = joblib.load(model_path)

try:
    loaded_model = joblib.load(model_path)
    model = loaded_model['model']
    preprocessor = loaded_model['preprocessor']
except Exception as e:
    print(f"Error loading the model: {e}")
    model = None
    preprocessor = None

# Define the features
numeric_features = ['ApplicantIncome', 'CoapplicantIncome', 'LoanAmount', 'Loan_Amount_Term', 'Credit_History']
categorical_features = ['Gender', 'Married', 'Dependents', 'Education', 'Self_Employed', 'Property_Area']

def predict_loan(features):
    if model is None or preprocessor is None:
        return "Error: Model or preprocessor not loaded"

    # Convert features to a DataFrame
    feature_names = numeric_features + categorical_features
    df = pd.DataFrame([features], columns=feature_names)
    
    try:
        # Preprocess the features
        X_preprocessed = preprocessor.transform(df)
        
        # Make prediction
        prediction = model.predict(X_preprocessed)
        return prediction[0]
    except Exception as e:
        print(f"Error during prediction: {e}")
        return "Error during prediction"