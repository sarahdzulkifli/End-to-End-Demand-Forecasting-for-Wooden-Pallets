"""Tests for XGBoost forecaster module."""
import pytest
import pandas as pd
import numpy as np
from src.models.xgboost_forecaster import XGBoostForecaster


class TestXGBoostForecaster:
    """Test cases for XGBoostForecaster class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.forecaster = XGBoostForecaster()
        
    def test_initialization(self):
        """Test that forecaster initializes with default config."""
        assert self.forecaster.config['n_estimators'] == 100
        assert self.forecaster.config['max_depth'] == 5
        assert self.forecaster.config['learning_rate'] == 0.1
        
    def test_initialization_with_custom_config(self):
        """Test that forecaster initializes with custom config."""
        custom_config = {'n_estimators': 50, 'max_depth': 3}
        forecaster = XGBoostForecaster(config=custom_config)
        
        assert forecaster.config['n_estimators'] == 50
        assert forecaster.config['max_depth'] == 3
        
    def test_prepare_features_returns_correct_shape(self):
        """Test that prepare_features returns correct shapes."""
        df = pd.DataFrame({
            'quantity': [100, 200, 300],
            'lag_1': [90, 110, 190],
            'lag_2': [80, 95, 105],
            'rolling_mean_3': [85, 100, 150],
            'posting_month': [1, 2, 3],
            'rate': [10.5, 11.0, 10.8]
        })
        
        X, y = self.forecaster.prepare_features(df)
        
        assert len(X) == 3
        assert len(y) == 3
        assert X.shape[1] > 0
        
    def test_prepare_features_handles_missing_columns(self):
        """Test that prepare_features handles missing feature columns."""
        df = pd.DataFrame({
            'quantity': [100, 200, 300],
            'lag_1': [90, 110, 190]
        })
        
        X, y = self.forecaster.prepare_features(df)
        
        assert 'lag_1' in X.columns
        assert len(y) == 3
        
    def test_fit_trains_model(self):
        """Test that fit method trains the model."""
        df = pd.DataFrame({
            'quantity': np.random.randint(50, 200, 100),
            'lag_1': np.random.randint(40, 190, 100),
            'lag_2': np.random.randint(30, 180, 100),
            'rolling_mean_3': np.random.randint(45, 195, 100),
            'posting_month': np.random.randint(1, 13, 100),
            'rate': np.random.uniform(10, 15, 100)
        })
        
        metrics = self.forecaster.fit(df, test_size=0.2)
        
        assert 'train' in metrics
        assert 'test' in metrics
        assert 'rmse' in metrics['test']
        assert 'mae' in metrics['test']
        assert 'r2' in metrics['test']
        assert metrics['test']['rmse'] >= 0
        
    def test_predict_returns_predictions(self):
        """Test that predict returns predictions."""
        # Train model first
        train_df = pd.DataFrame({
            'quantity': np.random.randint(50, 200, 100),
            'lag_1': np.random.randint(40, 190, 100),
            'lag_2': np.random.randint(30, 180, 100),
            'rolling_mean_3': np.random.randint(45, 195, 100),
            'posting_month': np.random.randint(1, 13, 100),
            'rate': np.random.uniform(10, 15, 100)
        })
        self.forecaster.fit(train_df)
        
        # Make predictions
        test_df = pd.DataFrame({
            'lag_1': [100, 110],
            'lag_2': [95, 105],
            'rolling_mean_3': [98, 108],
            'posting_month': [5, 6],
            'rate': [12.5, 13.0]
        })
        
        predictions = self.forecaster.predict(test_df)
        
        assert len(predictions) == 2
        assert all(predictions >= 0)
