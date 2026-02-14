"""Base forecaster class for demand forecasting models."""

from abc import ABC, abstractmethod
import pandas as pd
import numpy as np
from typing import Dict, Tuple
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


class BaseForecaster(ABC):
    """Abstract base class for forecasting models."""
    
    def __init__(self):
        self.model = None
        self.feature_columns = None
    
    @abstractmethod
    def fit(self, df: pd.DataFrame, test_size: float = 0.2) -> Dict:
        """
        Train the forecasting model.
        
        Args:
            df: Training data
            test_size: Proportion of data to use for testing
            
        Returns:
            Dictionary containing training metrics
        """
        pass
    
    @abstractmethod
    def predict(self, df: pd.DataFrame) -> np.ndarray:
        """
        Generate predictions for input data.
        
        Args:
            df: Input data for prediction
            
        Returns:
            Array of predictions
        """
        pass
    
    @abstractmethod
    def save(self, path: str):
        """
        Save model to disk.
        
        Args:
            path: Path to save the model
        """
        pass
    
    @abstractmethod
    def load(self, path: str):
        """
        Load model from disk.
        
        Args:
            path: Path to load the model from
        """
        pass
    
    def calculate_metrics(self, y_true: np.ndarray, y_pred: np.ndarray) -> Dict:
        """
        Calculate regression metrics.
        
        Args:
            y_true: True values
            y_pred: Predicted values
            
        Returns:
            Dictionary containing MAE, RMSE, MAPE, and R2 score
        """
        mae = mean_absolute_error(y_true, y_pred)
        rmse = np.sqrt(mean_squared_error(y_true, y_pred))
        r2 = r2_score(y_true, y_pred)
        
        # Calculate MAPE (Mean Absolute Percentage Error)
        # Avoid division by zero by filtering out zero values
        mask = y_true != 0
        if mask.sum() > 0:
            mape = np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100
        else:
            mape = 0.0
        
        return {
            'mae': mae,
            'rmse': rmse,
            'mape': mape,
            'r2': r2
        }
