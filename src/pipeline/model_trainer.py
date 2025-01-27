from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
import pandas as pd
import numpy as np
from typing import Tuple, Dict
import joblib


def train_model(X: pd.DataFrame, y: pd.Series) -> Tuple[RandomForestClassifier, Dict, pd.Series]:
    # Define the model and parameter grid
    base_model = RandomForestClassifier(random_state=42)
    param_grid = {
        'n_estimators': [100, 200, 300],
        'max_depth': [None, 10, 20],
        'min_samples_split': [2, 5],
        'min_samples_leaf': [1, 2]
    }

    # Perform grid search
    grid_search = GridSearchCV(base_model, param_grid, cv=5, scoring='roc_auc', n_jobs=-1)
    grid_search.fit(X, y)

    # Get feature importances
    feature_importances = pd.Series(
        grid_search.best_estimator_.feature_importances_,
        index=X.columns
    ).sort_values(ascending=False)

    results = {
        'best_params': grid_search.best_params_,
        'best_score': grid_search.best_score_
    }

    return grid_search.best_estimator_, results, feature_importances
