# End-to-End Inventory Demand Forecasting for Wooden Pallets [WORK IN PROGRESS]

## Project Introduction
Managing efficient inventory is key for businesses in today's fast-paced market in order to keep customers happy.
The main goal is to improve inventory management through demand prediction for wooden pallets, in which play important role in shipping and logistics.
This will help us allocate resources more efficiently and reduce inventory storage wastage.

## Dataset & Features
- Data Overview: Transactional data for wooden pallet.
- Data Source: Company records.
- Total record: 1582
- Total features: 33
- Key features:
  Dates: Posting, Effective and Sales Order (SO) Dates.
  Customer & Vendor Info: Codes, Names, and Types.
  Warehouse Details: Source and Destination.
  Product Info: Category, Item Code.
  Transaction Details: Quantity, Rate and Unit.
  Logistics: Document Type, Vehicle Type, Dispatch Status
  Categorical Insights: Region, LOB, BP Type.

## Exploratory Data Analysis (EDA)
### Purpose
- Data cleaning & preprocessing.
- Outlier detection & missing data handling.
- Key patterns, relationships & distributions in data.
- Univariate & bivariate analysis.

### Key Findings
- Features with 100% of missing values are dropped.
- We feature engineered the data with volatility and observed key customers exhibit higher demand variability, emphasizing the need for improved communication or forecasting for their accounts.
- We observed a seasonal pattern in demand, with higher sales during certain months.
- We figured high-demand and low-demand regions suggesting the need for region-specific inventory policies, for instance, regions with low demand may benefit from centralized stocking to minimize logistics costs.
- We identified relationships between variables in dataset to find strong correlations which indicating potential predictors for demand.

## Modeling Approach
- We experimented with multiple forecasting models, including ARIMA, SARIMA, Prophet and XGBoost, to identify the best-performing approach.

## Results
- Best model: XGBoost
- Reason:
  Outperformed other models in MAE, RMSE, and MAPE.
  Effective at handling complex relationships between lagged and rolling features.
  Flexible and scalable for deployment.
- Managed to forecast demand of wooden pallets for incoming 6-months.

## Next Step
Next steps include deploying the model using in EC2 with app runner.
