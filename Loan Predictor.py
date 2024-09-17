import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score, RandomizedSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from xgboost import XGBClassifier
import joblib


#Load data
df = pd.read_csv('/home/martinmuti/Downloads/df1_loan.csv')
df

# Data cleaning and preprocessing
def preprocess_data(df):
    # Remove $ sign from Total_Income and convert to float
    df['Total_Income'] = df['Total_Income'].str.replace('$', '').astype(float)
    
    # Drop Loan_ID column
    df = df.drop('Loan_ID', axis=1)
    
    # Handle Dependents column
    df['Dependents'] = df['Dependents'].replace('3+', '3')
    df['Dependents'] = pd.to_numeric(df['Dependents'])
    
    # Convert categorical columns to category dtype
    categorical_columns = ['Gender', 'Married', 'Education', 'Self_Employed', 'Property_Area']
    for col in categorical_columns:
        df[col] = df[col].astype('category')
    
    # Convert numeric columns to float
    numeric_columns = ['ApplicantIncome', 'CoapplicantIncome', 'LoanAmount', 'Loan_Amount_Term', 'Credit_History']
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Encode the target variable
    df['Loan_Status'] = df['Loan_Status'].map({'N': 0, 'Y': 1})
    
    # Remove rows with missing values
    df = df.dropna()
    
    return df

df = preprocess_data(df)

def perform_eda(df):
    # Distribution of target variable
    plt.figure(figsize=(8, 6))
    sns.countplot(x='Loan_Status', data=df)
    plt.title('Distribution of Loan Status')
    plt.show()
    
    # Correlation heatmap for numeric columns only
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    plt.figure(figsize=(12, 10))
    sns.heatmap(df[numeric_columns].corr(), annot=True, cmap='coolwarm')
    plt.title('Correlation Heatmap (Numeric Features)')
    plt.show()
    
    # Distribution of numerical features
    numerical_features = ['ApplicantIncome', 'CoapplicantIncome', 'LoanAmount', 'Loan_Amount_Term', 'Total_Income']
    fig, axes = plt.subplots(3, 2, figsize=(15, 15))
    for i, feature in enumerate(numerical_features):
        sns.histplot(df[feature], kde=True, ax=axes[i//2, i%2])
    plt.tight_layout()
    plt.show()
    
    # Categorical features vs Loan Status
    categorical_features = ['Gender', 'Married', 'Education', 'Self_Employed', 'Property_Area']
    fig, axes = plt.subplots(3, 2, figsize=(15, 15))
    for i, feature in enumerate(categorical_features):
        sns.countplot(x=feature, hue='Loan_Status', data=df, ax=axes[i//2, i%2])
        axes[i//2, i%2].set_xticklabels(axes[i//2, i%2].get_xticklabels(), rotation=45)
    plt.tight_layout()
    plt.show()

    # Print summary statistics
    print(df.describe())
    
    # Print info about the dataset
    print(df.info())

perform_eda(df)


# Prepare data for modeling
X = df.drop('Loan_Status', axis=1)
y = df['Loan_Status']

# Encode the target variable
le = LabelEncoder()
y = le.fit_transform(y)

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define preprocessing steps
numeric_features = ['ApplicantIncome', 'CoapplicantIncome', 'LoanAmount', 'Loan_Amount_Term', 'Credit_History', 'Total_Income', 'Dependents']
categorical_features = ['Gender', 'Married', 'Education', 'Self_Employed', 'Property_Area']

numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(drop='first', handle_unknown='ignore'))
])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ])

# Define models
models = {
    'Logistic Regression': LogisticRegression(random_state=42),
    'Random Forest': RandomForestClassifier(random_state=42),
    'XGBoost': XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)
}

def train_evaluate_models(models, X_train, X_test, y_train, y_test, le):
    results = {}
    for name, model in models.items():
        pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                                   ('classifier', model)])
        
        # Fit the pipeline
        pipeline.fit(X_train, y_train)
        
        # Make predictions
        y_pred = pipeline.predict(X_test)
        
        # Convert class labels to strings
        target_names = [str(class_) for class_ in le.classes_]
        
        # Store results
        results[name] = {
            'accuracy': accuracy_score(y_test, y_pred),
            'classification_report': classification_report(y_test, y_pred, target_names=target_names),
            'confusion_matrix': confusion_matrix(y_test, y_pred),
            'pipeline': pipeline
        }
        
        # Print results
        print(f"\n{name} Results:")
        print(f"Accuracy: {results[name]['accuracy']:.4f}")
        print("\nClassification Report:")
        print(results[name]['classification_report'])
        print("\nConfusion Matrix:")
        print(results[name]['confusion_matrix'])
        
        # Cross-validation
        cv_scores = cross_val_score(pipeline, X, y, cv=5, scoring='accuracy')
        print(f"\nCross-Validation Accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
    
    return results

results = train_evaluate_models(models, X_train, X_test, y_train, y_test, le)

# Hyperparameter tuning for the best model
best_model_name = max(results, key=lambda x: results[x]['accuracy'])
best_model = models[best_model_name]

if best_model_name == 'Random Forest':
    param_dist = {
        'classifier__n_estimators': [100, 200, 300],
        'classifier__max_depth': [None, 5, 10, 15],
        'classifier__min_samples_split': [2, 5, 10],
        'classifier__min_samples_leaf': [1, 2, 4]
    }
elif best_model_name == 'XGBoost':
    param_dist = {
        'classifier__n_estimators': [100, 200, 300],
        'classifier__max_depth': [3, 4, 5],
        'classifier__learning_rate': [0.01, 0.1, 0.3],
        'classifier__subsample': [0.6, 0.8, 1.0]
    }
else:  # Logistic Regression
    param_dist = {
        'classifier__C': [0.001, 0.01, 0.1, 1, 10, 100],
        'classifier__penalty': ['l2'],
        'classifier__solver': ['lbfgs', 'newton-cg', 'sag']
    }

pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                           ('classifier', best_model)])

random_search = RandomizedSearchCV(estimator=pipeline, param_distributions=param_dist, 
                                   n_iter=100, cv=5, verbose=2, random_state=42, n_jobs=-1)
random_search.fit(X, y)

print("Best parameters found:", random_search.best_params_)
print("Best cross-validation score:", random_search.best_score_)

# Feature importance (for Random Forest or XGBoost)
if best_model_name in ['Random Forest', 'XGBoost']:
    feature_names = (numeric_features + 
                     [f"{feature}_{category}" for feature, categories in 
                      random_search.best_estimator_.named_steps['preprocessor'].named_transformers_['cat'].named_steps['onehot'].categories_ 
                      for category in categories[1:]])
    
    importances = random_search.best_estimator_.named_steps['classifier'].feature_importances_
    feature_importances = pd.Series(importances, index=feature_names).sort_values(ascending=False)
    
    plt.figure(figsize=(10, 6))
    feature_importances.head(10).plot(kind='bar')
    plt.title('Top 10 Feature Importances')
    plt.tight_layout()
    plt.show()

    # Final model evaluation
final_model = random_search.best_estimator_
y_pred = final_model.predict(X_test)

# Convert class labels to strings
target_names = [str(class_) for class_ in le.classes_]

print("\nFinal Model Evaluation:")
print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=target_names))
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))