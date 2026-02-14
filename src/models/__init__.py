"""Models package for demand forecasting."""

from .base import BaseForecaster
from .xgboost_forecaster import XGBoostForecaster

__all__ = ['BaseForecaster', 'XGBoostForecaster']
