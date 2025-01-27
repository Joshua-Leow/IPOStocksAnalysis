import pandas as pd
from matplotlib import pyplot as plt

from src.config import selected_attributes
from src.pipeline.data_loader import fetch_stock_data, fetch_stock_info, calculate_returns
from src.pipeline.feature_engineering import prepare_features
from src.pipeline.model_evaluator import evaluate_predictions
from src.pipeline.model_trainer import train_model


def main():
    symbols = ['AAPL', 'MSFT', 'META', 'ADBE', 'BABA', 'SPY', 'TSLA', 'RYI', 'TTOO']

    print("1. Fetching stock data...")
    stock_data = fetch_stock_data(symbols)

    print("\n2. Fetching stock information...")
    stock_info = fetch_stock_info(symbols, selected_attributes)

    print("\n3. Preparing features...")
    X, feature_names = prepare_features(stock_data, stock_info, selected_attributes)

    # Calculate returns for target period (year 5-6)
    target_returns = calculate_returns(stock_data, 1250, 1500)

    # Prepare target variable (1 for top 30% performers)
    threshold = target_returns.quantile(0.7)
    y = (target_returns >= threshold).astype(int)

    print("\n4. Training model...")
    model, training_results, feature_importances = train_model(X, y)

    print("\n5. Evaluating predictions...")
    predictions = pd.Series(model.predict_proba(X)[:, 1], index=X.index)
    evaluation, performance_report = evaluate_predictions(y, predictions, target_returns)

    # Print results
    print("\n=== Model Training Results ===")
    print(f"Best Parameters: {training_results['best_params']}")
    print(f"Cross-validation Score (ROC AUC): {training_results['best_score']:.4f}")

    print("\n=== Model Evaluation ===")
    print(f"ROC AUC Score: {evaluation['roc_auc']:.4f}")
    print(f"Precision: {evaluation['precision']:.4f}")
    print(f"Recall: {evaluation['recall']:.4f}")

    print("\n=== Portfolio Performance ===")
    print(f"Average Return of Top 30% Predicted Stocks: {evaluation['avg_return_predicted_top']:.2f}%")
    print(f"Average Return of All Stocks: {evaluation['avg_return_all_stocks']:.2f}%")
    print(f"Portfolio Outperformance: {evaluation['portfolio_outperformance']:.2f}%")

    print("\n=== Top 10 Most Important Features ===")
    print(feature_importances.head(10))

    print("\n=== Top 5 Predicted Performers ===")
    print(performance_report.head())

    # Plot feature importance
    plt.figure(figsize=(12, 6))
    feature_importances.head(10).plot(kind='bar')
    plt.title('Top 10 Most Important Features')
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()