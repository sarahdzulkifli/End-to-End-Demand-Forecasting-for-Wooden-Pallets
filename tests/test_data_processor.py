"""Tests for data processor module."""
import pytest
import pandas as pd
import numpy as np
from src.data.processor import DataProcessor


class TestDataProcessor:
    """Test cases for DataProcessor class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.processor = DataProcessor()
        
    def test_clean_data_drops_unnecessary_columns(self):
        """Test that clean_data drops unnecessary columns."""
        df = pd.DataFrame({
            'quantity': [100, 200, 300],
            'Comments': ['test', 'test', 'test'],
            'U_GRNNO': ['A', 'B', 'C']
        })
        
        result = self.processor.clean_data(df)
        
        assert 'quantity' in result.columns
        assert 'Comments' not in result.columns
        assert 'U_GRNNO' not in result.columns
        
    def test_clean_data_removes_duplicates(self):
        """Test that clean_data removes duplicate rows."""
        df = pd.DataFrame({
            'quantity': [100, 100, 200],
            'product': ['A', 'A', 'B']
        })
        
        result = self.processor.clean_data(df)
        
        assert len(result) == 2
        
    def test_clean_data_formats_column_names(self):
        """Test that column names are properly formatted."""
        df = pd.DataFrame({
            'Product Name': [1, 2, 3],
            'Total Quantity': [100, 200, 300]
        })
        
        result = self.processor.clean_data(df)
        
        assert 'product_name' in result.columns
        assert 'total_quantity' in result.columns
        assert 'Product Name' not in result.columns
        
    def test_convert_datatypes_handles_dates(self):
        """Test that date columns are converted correctly."""
        df = pd.DataFrame({
            'posting_date': ['2024-01-01', '2024-01-02'],
            'quantity': [100, 200]
        })
        
        result = self.processor.convert_datatypes(df)
        
        assert pd.api.types.is_datetime64_any_dtype(result['posting_date'])
        
    def test_convert_datatypes_handles_invalid_dates(self):
        """Test that invalid dates are handled gracefully."""
        df = pd.DataFrame({
            'posting_date': ['invalid', '2024-01-02'],
            'quantity': [100, 200]
        })
        
        result = self.processor.convert_datatypes(df)
        
        assert pd.api.types.is_datetime64_any_dtype(result['posting_date'])
        assert pd.isna(result['posting_date'].iloc[0])
