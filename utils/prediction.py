from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd

def prepare_features(df):
    """Prepare features for prediction model."""
    # Convert day of week to numeric (0 = Monday, 6 = Sunday)
    day_mapping = {
        'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3,
        'Friday': 4, 'Saturday': 5, 'Sunday': 6
    }

    X = pd.DataFrame({
        'hour': df['hour'],
        'day_of_week': df['day_of_week'].map(day_mapping)
    })
    y = df['traffic_volume']
    return X, y

def train_prediction_model(df):
    """Train a simple RandomForest model for traffic prediction."""
    X, y = prepare_features(df)

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Train model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Calculate performance
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)

    return model, train_score, test_score

def predict_next_day(model, last_day_data):
    """Predict traffic for the next 24 hours."""
    # Get the day of week for predictions
    day_mapping = {
        'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3,
        'Friday': 4, 'Saturday': 5, 'Sunday': 6
    }

    last_day = last_day_data['day_of_week'].iloc[-1]
    day_num = day_mapping[last_day]

    next_day = pd.DataFrame({
        'hour': range(24),
        'day_of_week': [day_num] * 24
    })

    predictions = model.predict(next_day)
    return predictions