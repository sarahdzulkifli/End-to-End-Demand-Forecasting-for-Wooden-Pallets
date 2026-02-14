import sys
sys.path.append('.')

import pandas as pd
from loguru import logger
from src.data.processor import DataProcessor
from src.models.xgboost_forecaster import XGBoostForecaster
from pathlib import Path

def main():
    """Train and save the demand forecasting model."""
    
    logger.info("Starting model training pipeline")
    
    # Load data
    data_path = "data/raw/DOC-20241224-WA0017..xlsx"  
    logger.info(f"Loading data from {data_path}")
    df = pd.read_excel(data_path)
    
    # Process data
    processor = DataProcessor()
    processed_df = processor.process(df)
    logger.info(f"Data processed: {processed_df.shape}")
    
    # Train model
    model = XGBoostForecaster(config={
        'n_estimators': 100,
        'max_depth': 5,
        'learning_rate': 0.1,
        'subsample': 0.8,
        'random_state': 42
    })
    
    metrics = model.fit(processed_df)
    
    # Log metrics
    logger.info("Training Metrics:")
    logger.info(f"  Train MAE: {metrics['train']['mae']:.2f}")
    logger.info(f"  Train RMSE: {metrics['train']['rmse']:.2f}")
    logger.info(f"  Test MAE: {metrics['test']['mae']:.2f}")
    logger.info(f"  Test RMSE: {metrics['test']['rmse']:.2f}")
    logger.info(f"  Test MAPE: {metrics['test']['mape']:.2f}%")
    
    # Save model
    model_path = Path("models/xgboost_model.pkl")
    model_path.parent.mkdir(parents=True, exist_ok=True)
    model.save(str(model_path))
    
    logger.info("Model training complete!")
    
    return metrics

if __name__ == "__main__":
    metrics = main()