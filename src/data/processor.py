import pandas as pd
import numpy as np
from typing import Tuple
from loguru import logger

class DataProcessor:
    """Process and prepare data for forecasting models."""
    
    def __init__(self):
        self.feature_columns = None
        
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean raw data."""
        logger.info("Starting data cleaning")
        
        # Drop unnecessary columns
        columns_to_drop = [
            'Comments', 'U_GRNNO', 'Loading/Unloading', 
            'Detention', 'KITITEM', 'U_AssetClass', 'numatcard'
        ]
        df = df.drop(columns=columns_to_drop, errors='ignore')
        
        # Clean column names
        df.columns = df.columns.str.strip().str.replace(' ', '_').str.lower()
        
        # Remove duplicates
        df = df.drop_duplicates()
        
        logger.info(f"Cleaned data shape: {df.shape}")
        return df
    
    def convert_datatypes(self, df: pd.DataFrame) -> pd.DataFrame:
        """Convert columns to appropriate data types."""
        logger.info("Converting data types")
        
        # Date columns
        date_columns = ['posting_date', 'effective_date', 'create_date', 
                       'so_creation_date', 'so_due_date']
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
        
        # Numerical columns
        if 'quantity' in df.columns:
            df['quantity'] = df['quantity'].astype(int)
        if 'rate' in df.columns:
            df['rate'] = df['rate'].astype(float)
        
        # Categorical columns
        categorical_cols = ['lob', 'region', 'bp_type', 'product_category']
        for col in categorical_cols:
            if col in df.columns:
                df[col] = df[col].astype('category')
        
        return df
    
    def engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create derived features."""
        logger.info("Engineering features")
        
        # Time-based features
        if 'posting_date' in df.columns:
            df['posting_day_of_week'] = df['posting_date'].dt.day_name()
            df['posting_month'] = df['posting_date'].dt.month
            df['posting_year'] = df['posting_date'].dt.year
            df['posting_quarter'] = df['posting_date'].dt.quarter
            df['is_posting_weekend'] = df['posting_date'].dt.dayofweek >= 5
            df['is_posting_month_end'] = df['posting_date'].dt.is_month_end
        
        # Lead time calculation
        if 'so_due_date' in df.columns and 'so_creation_date' in df.columns:
            df['lead_time'] = (df['so_due_date'] - df['so_creation_date']).dt.days
        
        # Lag features for time series
        if 'quantity' in df.columns:
            df['lag_1'] = df['quantity'].shift(1)
            df['lag_2'] = df['quantity'].shift(2)
            df['rolling_mean_3'] = df['quantity'].rolling(window=3).mean()
        
        return df
    
    def add_volatility_flag(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add customer volatility indicator."""
        logger.info("Calculating volatility flags")
        
        if 'customer/vendor_code' not in df.columns or 'quantity' not in df.columns:
            return df
        
        volatility_df = df.groupby('customer/vendor_code')['quantity'].agg(
            ['mean', 'std']
        ).reset_index()
        
        volatility_df['cv'] = volatility_df['std'] / volatility_df['mean']
        volatility_df['volatility_flag'] = (volatility_df['cv'] > 0.5).astype(int)
        
        df = df.merge(
            volatility_df[['customer/vendor_code', 'volatility_flag']], 
            on='customer/vendor_code', 
            how='left'
        )
        
        return df
    
    def process(self, df: pd.DataFrame) -> pd.DataFrame:
        """Full processing pipeline."""
        df = self.clean_data(df)
        df = self.convert_datatypes(df)
        df = self.engineer_features(df)
        df = self.add_volatility_flag(df)
        
        # Drop rows with NaN in target or critical features only
        # Don't drop all NaN values as lag features will have some NaN
        critical_columns = ['quantity']
        if 'posting_date' in df.columns:
            critical_columns.append('posting_date')
        
        df = df.dropna(subset=critical_columns)
        
        logger.info(f"Final processed data shape: {df.shape}")
        return df