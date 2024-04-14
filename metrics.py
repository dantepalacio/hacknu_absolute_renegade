from sklearn.metrics import mean_squared_error, mean_absolute_error, mean_absolute_percentage_error
from scipy.stats import pearsonr
from sklearn.metrics import r2_score
import json
import numpy as np

def getJsonMetrics(y_data, y_pred): 
    mse = mean_squared_error(y_data, y_pred)
    mae = mean_absolute_error(y_data, y_pred)
    corr_coeff, _ = pearsonr(y_data.flatten(), y_pred)
    r2 = r2_score(y_data, y_pred)

    mape = None
    # Calculate MAPE if there are no zeros in y_data
    if not (y_data == 0).any():
        absolute_percentage_errors = np.abs((y_data - y_pred) / y_data)
        mape = np.mean(absolute_percentage_errors) * 100

    return {
        "MSE": mse,
        "MAE": mae,
        "MAPE": mape,
        "Correlation Coefficient": corr_coeff,
        "R^2": r2
    }

def metrics_to_json(metrics):
    return json.dumps(metrics)

def json_to_metrics(json_str):
    return json.loads(json_str)

def getMetrics(y_data, y_pred): 
    mse = mean_squared_error(y_data, y_pred)
    mae = mean_absolute_error(y_data, y_pred)
    mape = mean_absolute_percentage_error(y_data, y_pred)
    corr_coeff, _ = pearsonr(y_data.flatten(), y_pred)
    r2 = r2_score(y_data, y_pred)
    return mse, mae, mape, corr_coeff, r2

def printMetrics(y_data, y_pred):
    mse = mean_squared_error(y_data, y_pred)
    mae = mean_absolute_error(y_data, y_pred)
    mape = mean_absolute_percentage_error(y_data, y_pred)
    corr_coeff, _ = pearsonr(y_data.flatten(), y_pred)
    r2 = r2_score(y_data, y_pred)
    print("Mean Squared Error (MSE):", mse)
    print("Mean Absolute Error (MAE):", mae)
    print("Mean absolute percentage error (MAPE):", mape)
    print("Correlation Coefficient:", corr_coeff)
    print("Determination Coefficient (R^2):", r2)

def getMSE(y_data, y_pred):
    metric_value = mean_squared_error(y_data, y_pred)
    return metric_value

def getMAE(y_data, y_pred):
    metric_value = mean_squared_error(y_data, y_pred)
    return metric_value

def getMAPE(y_data, y_pred):
    metric_value = mean_squared_error(y_data, y_pred)
    return metric_value

def getCorrelation(y_data, y_pred):
    metric_value = mean_squared_error(y_data, y_pred)
    return metric_value

def getR2(y_data, y_pred):
    metric_value = mean_squared_error(y_data, y_pred)
    return metric_value