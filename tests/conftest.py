"""Pytest configuration and shared fixtures."""
import pytest
import pandas as pd
import numpy as np


@pytest.fixture
def sample_dataframe():
    """Create a sample DataFrame for testing."""
    np.random.seed(42)
    return pd.DataFrame({
        'quantity': np.random.randint(50, 200, 100),
        'lag_1': np.random.randint(40, 190, 100),
        'lag_2': np.random.randint(30, 180, 100),
        'rolling_mean_3': np.random.randint(45, 195, 100),
        'posting_month': np.random.randint(1, 13, 100),
        'posting_quarter': np.random.randint(1, 5, 100),
        'rate': np.random.uniform(10, 15, 100),
        'u_frt': np.random.uniform(400, 600, 100),
        'lead_time': np.random.randint(1, 14, 100),
        'posting_date': pd.date_range('2024-01-01', periods=100, freq='D')
    })


@pytest.fixture
def sample_prediction_data():
    """Create sample data for predictions."""
    return pd.DataFrame({
        'lag_1': [100, 110, 120],
        'lag_2': [95, 105, 115],
        'rolling_mean_3': [98, 108, 118],
        'posting_month': [5, 6, 7],
        'posting_quarter': [2, 2, 3],
        'rate': [12.5, 13.0, 12.8],
        'u_frt': [500, 520, 510],
        'lead_time': [7, 8, 6]
    })
