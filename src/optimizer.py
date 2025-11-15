# File: src/optimizer.py

import pandas as pd
import numpy as np

def find_optimal_price(ride_details, model, min_price=15, max_price=150, steps=100):
    """
    Simulates a range of prices to find the one that maximizes revenue.

    ride_details: A dictionary with all features EXCEPT 'Price'.
    model: The pre-trained model pipeline.
    """

    # 1. Create a "test" DataFrame with our ride details
    test_data = pd.DataFrame([ride_details])

    # 2. Create a range of prices to test
    price_range = np.linspace(min_price, max_price, steps)

    # 3. Build a DataFrame for all price points
    simulation_df = pd.concat([test_data] * len(price_range), ignore_index=True)
    simulation_df['Price'] = price_range

    # 4. Predict demand for ALL prices at once
    predicted_demand = model.predict(simulation_df)

    # 5. Calculate revenue for each price
# First, assign the numpy array to the new column
    simulation_df['Predicted_Demand'] = predicted_demand

    # Now, use the PANDAS .clip() method on that column
    simulation_df['Predicted_Demand'] = simulation_df['Predicted_Demand'].clip(lower=0)

    # Now, calculate revenue
    simulation_df['Revenue'] = simulation_df['Price'] * simulation_df['Predicted_Demand']

    # 6. Find the optimal price
    optimal_row = simulation_df.loc[simulation_df['Revenue'].idxmax()]

    # Convert to a standard dictionary for JSON compatibility
    return optimal_row.to_dict()