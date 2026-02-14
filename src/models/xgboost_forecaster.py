import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
import joblib
from typing import Dict, Tuple
from loguru import logger
from .base import BaseForecaster

class XGBoostForecaster(BaseForecaster):
    """XGBoost-based demand forecasting model."""
    
    def __init__(self, config: Dict = None):
        super().__init__()
        self.config = config or {
            'n_estimators': 100,
            'max_depth': 5,
            'learning_rate': 0.1,
            'subsample': 0.8,
            'random_state': 42
        }
        self.model = XGBRegressor(**self.config)
        self.feature_columns = None
        
    def prepare_features(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
        """Prepare features and target for training."""
        feature_cols = [
            'lag_1', 'lag_2', 'rolling_mean_3', 
            'posting_month', 'rate', 'u_frt', 
            'posting_quarter', 'lead_time'
        ]
        
        # Filter available columns
        available_features = [col for col in feature_cols if col in df.columns]
        self.feature_columns = available_features
        
        X = df[available_features]
        y = df['quantity'] if 'quantity' in df.columns else None
        
        return X, y
    
    def fit(self, df: pd.DataFrame, test_size: float = 0.2) -> Dict:
        """Train the model."""
        logger.info("Training XGBoost model")
        
        X, y = self.prepare_features(df)
        
        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42
        )
        
        # Train model
        self.model.fit(X_train, y_train)
        
        # Evaluate
        train_pred = self.model.predict(X_train)
        test_pred = self.model.predict(X_test)
        
        metrics = {
            'train': self.calculate_metrics(y_train, train_pred),
            'test': self.calculate_metrics(y_test, test_pred)
        }
        
        logger.info(f"Training complete. Test MAE: {metrics['test']['mae']:.2f}")
        
        return metrics
    
    def predict(self, df: pd.DataFrame) -> np.ndarray:
        """Generate predictions."""
        if self.feature_columns is None:
            raise ValueError("Model not trained. Call fit() first.")
        
        X, _ = self.prepare_features(df)
        predictions = self.model.predict(X)
        
        return predictions
    
    def forecast_future(self, last_known_data: pd.Series, periods: int = 6) -> pd.DataFrame:
        """Forecast future periods."""
        logger.info(f"Forecasting {periods} periods ahead")
        
        predictions = []
        current_data = last_known_data.copy()
        
        for i in range(periods):
            # Prepare input features
            input_features = pd.DataFrame({
                'lag_1': [current_data['quantity']],
                'lag_2': [current_data.get('lag_1', current_data['quantity'])],
                'rolling_mean_3': [current_data['quantity']],
                'posting_month': [(current_data['posting_month'] % 12) + 1],
                'rate': [current_data.get('rate', 0)],
                'u_frt': [current_data.get('u_frt', 0)],
                'posting_quarter': [((current_data['posting_month'] % 12) // 3) + 1],
                'lead_time': [current_data.get('lead_time', 7)]
            })
            
            # Predict
            pred = self.model.predict(input_features)[0]
            predictions.append(pred)
            
            # Update for next iteration
            current_data['lag_2'] = current_data.get('lag_1', current_data['quantity'])
            current_data['lag_1'] = current_data['quantity']
            current_data['quantity'] = pred
            current_data['posting_month'] = (current_data['posting_month'] % 12) + 1
        
        # Create forecast dataframe
        forecast_dates = pd.date_range(
            start=pd.Timestamp.now().replace(day=1),
            periods=periods,
            freq='MS'
        )
        
        forecast_df = pd.DataFrame({
            'date': forecast_dates,
            'predicted_quantity': predictions,
            'model': 'XGBoost'
        })
        
        return forecast_df
    
    def save(self, path: str):
        """Save model to disk."""
        model_data = {
            'model': self.model,
            'feature_columns': self.feature_columns,
            'config': self.config
        }
        joblib.dump(model_data, path)
        logger.info(f"Model saved to {path}")
    
    def load(self, path: str):
        """Load model from disk."""
        model_data = joblib.load(path)
        self.model = model_data['model']
        self.feature_columns = model_data['feature_columns']
        self.config = model_data['config']
        logger.info(f"Model loaded from {path}")