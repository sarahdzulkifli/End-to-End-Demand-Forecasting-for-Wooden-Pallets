from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io
from typing import List
from loguru import logger
from .schemas import PredictionRequest, PredictionResponse, HealthResponse
from ..models.xgboost_forecaster import XGBoostForecaster
from ..data.processor import DataProcessor

# Initialize app
app = FastAPI(
    title="Demand Forecasting API",
    description="API for wooden pallet demand forecasting",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
processor = DataProcessor()
model = XGBoostForecaster()

# Load pre-trained model
try:
    model.load("models/xgboost_model.pkl")
    logger.info("Model loaded successfully")
except Exception as e:
    logger.warning(f"Could not load model: {e}")

@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint."""
    return {
        "status": "healthy",
        "message": "Demand Forecasting API is running",
        "version": "1.0.0"
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "message": "API is operational",
        "version": "1.0.0"
    }

@app.post("/predict", response_model=List[PredictionResponse])
async def predict(request: PredictionRequest):
    """Generate demand forecast."""
    try:
        logger.info(f"Prediction request for {request.periods} periods")
        
        # Create last known data
        last_known = pd.Series({
            'quantity': request.last_quantity,
            'lag_1': request.last_quantity,
            'posting_month': request.current_month,
            'rate': request.rate,
            'u_frt': request.freight_cost
        })
        
        # Generate forecast
        forecast = model.forecast_future(last_known, periods=request.periods)
        
        # Convert to response format
        response = [
            PredictionResponse(
                date=row['date'].strftime('%Y-%m-%d'),
                predicted_quantity=float(row['predicted_quantity']),
                model='XGBoost'
            )
            for _, row in forecast.iterrows()
        ]
        
        return response
        
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload-and-predict")
async def upload_and_predict(file: UploadFile = File(...), periods: int = 6):
    """Upload data file and generate predictions."""
    try:
        # Read uploaded file
        contents = await file.read()
        df = pd.read_excel(io.BytesIO(contents))
        
        # Process data
        processed_df = processor.process(df)
        
        # Get last known values
        last_row = processed_df.iloc[-1]
        
        # Generate forecast
        forecast = model.forecast_future(last_row, periods=periods)
        
        return {
            "status": "success",
            "forecast": forecast.to_dict(orient='records')
        }
        
    except Exception as e:
        logger.error(f"Upload and predict error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/models")
async def list_models():
    """List available models."""
    return {
        "available_models": ["XGBoost", "Prophet", "ARIMA"],
        "default_model": "XGBoost"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)