import os
import pandas as pd
from DemandForecasting_WoodenPallets import logger
from xgboost import XGBRegressor
import joblib
from DemandForecasting_WoodenPallets.entity.config_entity import ModelTrainerConfig



class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.config = config

        
    def train(self):
        train_data = pd.read_excel(self.config.train_data_path)
        test_data = pd.read_excel(self.config.test_data_path)

        # Prepare your features and target variable
        train_x = train_data.drop(columns=[self.config.target_column])
        train_y = train_data[self.config.target_column]

        # Convert datetime columns to features or drop them
        train_x = self.preprocess_data(train_x)

        # Initialize and train the model
        xgb_model = XGBRegressor(random_state=42, n_estimators=100, enable_categorical=True)
        xgb_model.fit(train_x, train_y)

        # Save the model
        joblib.dump(xgb_model, os.path.join(self.config.root_dir, self.config.model_name))

    def preprocess_data(self, df):
        # Drop datetime columns or convert them to features
        df = df.drop(columns=['POSTING DATE', 'EFFECTIVE DATE', 'CREATE DATE', 'SO Creation Date', 'SO Due Date'], errors='ignore')

        # Convert categorical columns to 'category' type if not already
        categorical_columns = ['LOB', 'Region', 'BP TYPE', 'PRODUCT CATEGORY']
        for col in categorical_columns:
            if col in df.columns:
                df[col] = df[col].astype('category')

        # Return the processed DataFrame
        return df