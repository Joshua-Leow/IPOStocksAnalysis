import pandas as pd
import numpy as np
from sklearn.metrics import roc_auc_score, precision_score, recall_score, confusion_matrix
from typing import Dict, List, Tuple
import matplotlib.pyplot as plt
import seaborn as sns


def evaluate_predictions(y_true: pd.Series, y_pred_proba: pd.Series, actual_returns: pd.Series) -> Dict:
    # Convert probabilities to binary predictions (top 30% as positive class)
    threshold = np.percentile(y_pred_proba, 70)
    y_pred = (y_pred_proba >= threshold).astype(int)

    # Calculate metrics
    evaluation = {
        'roc_auc': roc_auc_score(y_true, y_pred_proba),
        'precision': precision_score(y_true, y_pred),
        'recall': recall_score(y_true, y_pred),
        'confusion_matrix': confusion_matrix(y_true, y_pred)
    }

    # Create performance report
    report = pd.DataFrame({
        'Actual_Return': actual_returns,
        'Predicted_Probability': y_pred_proba
    })

    # Sort by predicted probability
    report = report.sort_values('Predicted_Probability', ascending=False)

    # Calculate metrics for top 30% predicted performers
    n_top = int(len(report) * 0.3)
    top_predicted = report.head(n_top)

    # Add portfolio performance metrics
    evaluation.update({
        'avg_return_predicted_top': top_predicted['Actual_Return'].mean(),
        'avg_return_all_stocks': actual_returns.mean(),
        'portfolio_outperformance': top_predicted['Actual_Return'].mean() - actual_returns.mean()
    })

    return evaluation, report