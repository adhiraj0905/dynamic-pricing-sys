# File: main.py

import joblib
from fastapi import FastAPI
from pydantic import BaseModel

# Import our optimizer function
from src.optimizer import find_optimal_price

# --- 1. Initialize the FastAPI app ---
app = FastAPI(
    title="Dynamic Pricing API",
    description="API to find the optimal price for a ride.",
    version="0.1.0"
)

# --- 2. Load the Model ---
# This happens once, when the app starts up
try:
    model = joblib.load('models/demand_model_v1.joblib')
    print("Model loaded successfully!")
except FileNotFoundError:
    print("Error: Model file 'models/demand_model_v1.joblib' not found.")
    model = None
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

# --- 3. Define the Input Data Shape ---
# Pydantic validates the incoming data.
# These must match the columns our model was trained on (except 'Price' and 'Demand')
class RideRequest(BaseModel):
    Distance: float
    Time_of_Day: str  # e.g., "Morning", "Night"
    Weather: str      # e.g., "Clear", "Rainy"
    Base_Price: float
    Weather_Multiplier: float
    # Add any other features your model used

    # Example to show what the API expects
    class Config:
        json_schema_extra = {
            "example": {
                "Distance": 10.5,
                "Time_of_Day": "Afternoon",
                "Weather": "Clear",
                "Base_Price": 15.0,
                "Weather_Multiplier": 1.0
            }
        }

# --- 4. Create the API Endpoint ---
@app.get("/")
def read_root():
    return {"message": "Welcome to the Dynamic Pricing API. Go to /docs for details."}


@app.post("/optimize-price/")
async def optimize_price(request: RideRequest):
    """
    Receives ride details and returns the optimal price.
    """
    if model is None:
        return {"error": "Model not loaded. Check server logs."}

    # Convert Pydantic model to a dictionary
    ride_details = request.model_dump()

    try:
        # Call our optimizer
        optimal_result = find_optimal_price(ride_details, model)

        return {
            "message": "Optimal price calculated.",
            "optimal_price": optimal_result['Price'],
            "predicted_demand": optimal_result['Predicted_Demand'],
            "estimated_revenue": optimal_result['Revenue']
        }
    except Exception as e:
        return {"error": f"Error during optimization: {str(e)}"}