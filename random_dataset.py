#Generate random dataset
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random

def generate_time_series(start_date, end_date, freq='ME', trend='linear', noise_level=0.1):
    """
    Generate a time series dataset with two columns (Date and Value).
    
    Parameters:
        - start_date (str or datetime): Start date of the time series.
        - end_date (str or datetime): End date of the time series.
        - freq (str): Frequency of data points ('D' for days, 'M' for months, etc.).
        - trend (str): Type of trend to follow ('linear', 'exponential', 'sinusoidal', 'random').
        - noise_level (float): Level of noise to add to the trend.
        
    Returns:
        - Pandas DataFrame with two columns: 'Date' and 'Value'.
    """
    # Convert start_date and end_date to datetime objects if they are strings
    if isinstance(start_date, str):
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
    if isinstance(end_date, str):
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    
    dates = pd.date_range(start=start_date, end=end_date, freq=freq)
    values = []
    
    for i, date in enumerate(dates):
        if trend == 'linear':
            value = date.year * 12 + date.month  # Linear trend
        elif trend == 'exponential':
            value = 2 ** (date.year - start_date.year)  # Exponential trend
        elif trend == 'sinusoidal':
            value = 10 + 5 * (1 + np.sin((2 * np.pi * date.month / 12)))  # Sinusoidal trend
            value += i  # Linear trend
        elif trend == 'random':
            value = random.random() * 100  # Random values
        else:
            raise ValueError("Invalid trend type. Choose from 'linear', 'exponential', 'sinusoidal', or 'random'.")
        
        # Add noise
        value += random.gauss(0, noise_level * value)
        
        values.append(value)
    
    df = pd.DataFrame({'Date': dates, 'Value': values})
    return df

if __name__ == "__main__":
    # Generate time series data
    start_date = '2020-01-01'
    end_date = '2030-12-01'
    data = generate_time_series(start_date, end_date, freq='M', trend='linear', noise_level=0.1)

    # Save data to CSV
    data.to_csv('time_series_data.csv', index=False)