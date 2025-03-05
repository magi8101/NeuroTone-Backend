# src/train.py

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib
import os
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

# Get the absolute path to the project root directory
PROJECT_ROOT = Path(__file__).parent.parent
MODELS_DIR = PROJECT_ROOT / "models"
DATA_DIR = PROJECT_ROOT / "data"

def create_directories():
    """Create necessary directories if they don't exist"""
    MODELS_DIR.mkdir(exist_ok=True)
    DATA_DIR.mkdir(exist_ok=True)
    print(f"Created directories: {MODELS_DIR}, {DATA_DIR}")

def train_model():
    print("Starting model training...")
    
    # Read the CSV file
    data_file = DATA_DIR / "parkinsons.csv"
    try:
        df = pd.read_csv(data_file)
        print(f"Data loaded successfully. Shape: {df.shape}")
        
        # Print class distribution
        print("\nClass distribution:")
        print(df['status'].value_counts(normalize=True))
        
    except FileNotFoundError:
        print(f"Error: Could not find {data_file}")
        return None, None
    
    try:
        # Prepare features and target
        X = df.drop(['name', 'status'], axis=1)
        y = df['status']
        
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scale the features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Define parameter grid for GridSearchCV
        param_grid = {
            'n_estimators': [100, 200, 300],
            'max_depth': [None, 10, 20, 30],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4],
            'class_weight': [None, 'balanced']
        }
        
        # Create and train the model using GridSearchCV
        rf = RandomForestClassifier(random_state=42)
        grid_search = GridSearchCV(rf, param_grid, cv=5, scoring='balanced_accuracy')
        grid_search.fit(X_train_scaled, y_train)
        
        # Get the best model
        model = grid_search.best_estimator_
        
        # Print best parameters
        print("\nBest parameters:", grid_search.best_params_)
        
        # Make predictions
        y_pred = model.predict(X_test_scaled)
        
        # Print model performance
        print("\nModel Performance:")
        print("Accuracy:", accuracy_score(y_test, y_pred))
        print("\nConfusion Matrix:")
        print(confusion_matrix(y_test, y_pred))
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))
        
        # Feature importance analysis
        feature_importance = pd.DataFrame({
            'feature': X.columns,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)  # Changed from descending=True to ascending=False
        
        print("\nTop 10 Most Important Features:")
        print(feature_importance.head(10))
        
        # Plot feature importance
        plt.figure(figsize=(10, 6))
        sns.barplot(data=feature_importance.head(10), x='importance', y='feature')  # Changed order of x and y
        plt.title('Top 10 Most Important Features')
        plt.tight_layout()
        plt.savefig(PROJECT_ROOT / 'feature_importance.png')
        
        # Save the model and scaler
        joblib.dump(model, MODELS_DIR / "trained_model.joblib")
        joblib.dump(scaler, MODELS_DIR / "scaler.joblib")
        joblib.dump(X.columns.tolist(), MODELS_DIR / "feature_names.joblib")
        
        # Calculate and save feature thresholds
        healthy_thresholds = df[df['status'] == 0].describe()
        parkinsons_thresholds = df[df['status'] == 1].describe()
        
        feature_thresholds = {
            'healthy': {
                col: {
                    'mean': healthy_thresholds[col]['mean'],
                    'std': healthy_thresholds[col]['std'],
                    'min': healthy_thresholds[col]['min'],
                    'max': healthy_thresholds[col]['max']
                } for col in X.columns
            },
            'parkinsons': {
                col: {
                    'mean': parkinsons_thresholds[col]['mean'],
                    'std': parkinsons_thresholds[col]['std'],
                    'min': parkinsons_thresholds[col]['min'],
                    'max': parkinsons_thresholds[col]['max']
                } for col in X.columns
            }
        }
        
        joblib.dump(feature_thresholds, MODELS_DIR / "feature_thresholds.joblib")
        
        return model, scaler, feature_thresholds
        
    except Exception as e:
        print(f"Error during training: {str(e)}")
        return None, None, None

if __name__ == "__main__":
    print("=== Parkinson's Disease Detection Model Training ===\n")
    create_directories()
    model, scaler, thresholds = train_model()
    
    if model is not None:
        print("\nTraining completed successfully!")
        print("\nModel, scaler, and thresholds saved to:")
        print(f"- {MODELS_DIR / 'trained_model.joblib'}")
        print(f"- {MODELS_DIR / 'scaler.joblib'}")
        print(f"- {MODELS_DIR / 'feature_thresholds.joblib'}")
    else:
        print("\nTraining failed!")