import os
import pandas as pd
from DemandForecasting_WoodenPallets import logger
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from DemandForecasting_WoodenPallets.entity.config_entity import DataTransformationConfig



class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config

    def train_test_splitting(self):
        df = pd.read_excel(self.config.data_path)

        # EDA: Basic data cleaning and exploration
        df = df.drop_duplicates()
        df = df.drop("NumAtCard", axis=1)  # Drop 100% missing data for "NumAtCard" column
        df['POSTING DATE'] = pd.to_datetime(df['POSTING DATE'], errors='coerce')
        df['EFFECTIVE DATE'] = pd.to_datetime(df['EFFECTIVE DATE'], errors='coerce')
        df['CREATE DATE'] = pd.to_datetime(df['CREATE DATE'], errors='coerce')
        df['SO Creation Date'] = pd.to_datetime(df['SO Creation Date'])
        df['SO Due Date'] = pd.to_datetime(df['SO Due Date'])
        df['QUANTITY'] = df['QUANTITY'].astype(int)
        df['RATE'] = df['RATE'].astype(float)

        # Convert to 'category' type for categorical columns
        df['LOB'] = df['LOB'].astype('category')
        df['Region'] = df['Region'].astype('category')
        df['BP TYPE'] = df['BP TYPE'].astype('category')
        df['PRODUCT CATEGORY'] = df['PRODUCT CATEGORY'].astype('category')
        df['Customer/Vendor Code'] = df['Customer/Vendor Code'].astype(str)

        # Cleaning city and state columns
        df['City'] = df['City'].str.title()
        city_std = {'Vijaywada': 'Vijayawada'}
        state_std = {'Chattisgarh': 'Chhattisgarh'}

        df['City'] = df['City'].replace(city_std)
        df['STATE'] = df['STATE'].replace(state_std)

        # Extract features from the date columns
        df['posting_day_of_week'] = df['POSTING DATE'].dt.day_name()
        df['posting_month'] = df['POSTING DATE'].dt.month
        df['posting_year'] = df['POSTING DATE'].dt.year
        df['so_creation_year'] = df['SO Creation Date'].dt.year
        df['so_creation_month'] = df['SO Creation Date'].dt.month
        df['so_due_year'] = df['SO Due Date'].dt.year
        df['so_due_month'] = df['SO Due Date'].dt.month

        # Calculate the lead time (processing time)
        df['effective_to_posting'] = (df['EFFECTIVE DATE'] - df['POSTING DATE']).dt.days
        df['lead_time'] = (df['SO Due Date'] - df['SO Creation Date']).dt.days

        df['posting_quarter'] = df['POSTING DATE'].dt.quarter

        # Date falls on weekend
        df['is_posting_weekend'] = df['POSTING DATE'].dt.dayofweek >= 5

        # Inventory activity at month-end
        df['is_posting_month_end'] = df['POSTING DATE'].dt.is_month_end

        # Now split data into training and test sets (0.75, 0.25) split.
        train, test = train_test_split(df, test_size=0.25, random_state=42)

        # Continue with encoding categorical columns
        train_encoded, test_encoded = self.encode_categorical_columns(train, test)

        # Save the encoded data
        train_encoded.to_excel(os.path.join(self.config.root_dir, "train_encoded.xlsx"), index=False)
        test_encoded.to_excel(os.path.join(self.config.root_dir, "test_encoded.xlsx"), index=False)

        logger.info("Splitted data into training and test sets")
        logger.info(f"Train shape: {train_encoded.shape}")
        logger.info(f"Test shape: {test_encoded.shape}")

        print(train_encoded.shape)
        print(test_encoded.shape)

    def encode_categorical_columns(self, train_df, test_df):
        categorical_columns = train_df.select_dtypes(include=['object']).columns
        le = LabelEncoder()

    # Create a new DataFrame to hold the transformed data
        train_encoded = train_df.copy()
        test_encoded = test_df.copy()

        for col in categorical_columns:
            if train_df[col].nunique() < 10:  # Use one-hot for small unique categories
                # Fit on training data and transform both train and test
                dummies_train = pd.get_dummies(train_df[col], prefix=col, drop_first=True)
                dummies_test = pd.get_dummies(test_df[col], prefix=col, drop_first=True)

                # Align columns to ensure both DataFrames have the same columns
                dummies_train, dummies_test = dummies_train.align(dummies_test, join='outer', axis=1, fill_value=0)

                train_encoded = pd.concat([train_encoded, dummies_train], axis=1)
                test_encoded = pd.concat([test_encoded, dummies_test], axis=1)

                train_encoded.drop(col, axis=1, inplace=True)
                test_encoded.drop(col, axis=1, inplace=True)
            elif train_df[col].nunique() < 50:  # Use label encoding for mid-range categories
                # Fit the encoder on the training data
                train_encoded[col] = le.fit_transform(train_df[col].astype(str))
                # Transform the test data, handling unseen labels
                test_encoded[col] = test_df[col].astype(str).map(lambda x: le.transform([x])[0] if x in le.classes_ else -1)  # Map unseen labels to -1
            else:  # Use frequency encoding for high unique categories
                freq_map = train_df[col].value_counts().to_dict()
                train_encoded[col] = train_df[col].map(freq_map)
                test_encoded[col] = test_df[col].map(freq_map).fillna(0)  # Fill NaN with 0 or another value

        return train_encoded, test_encoded