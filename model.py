import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.optim import lr_scheduler
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from metrics import *
from data_visualize import *
from io import BytesIO
from PIL import Image
import io

class LSTM(nn.Module):
    def __init__(self, input_size=1, hidden_layer_size=100, output_size=1):
        super().__init__()
        self.hidden_layer_size = hidden_layer_size
        self.lstm1 = nn.LSTM(input_size, hidden_layer_size)
        self.linear = nn.Linear(hidden_layer_size, output_size)

    def forward(self, input_seq):
        lstm_out1, _ = self.lstm1(input_seq)
        predictions = self.linear(lstm_out1.view(len(input_seq), -1))
        return predictions[-1]
    
    def forecast(self, dataframe, future = 100, sequence_length = 300):
        if dataframe.shape[0] <= 1:
            print("Not enough data")
            return []
        self.eval()
        preds = []
        dataframe_tensor = torch.FloatTensor(dataframe).view(-1, 1)
        test_input = dataframe_tensor[-sequence_length:].view(-1, 1)
        with torch.no_grad():
            for i in range(future):
                pred = self(test_input[-sequence_length:].view(-1, 1))
                preds.append(pred.item())
                test_input = torch.cat((test_input, pred.view(-1, 1)))
        return preds
    
    def save(self, path):
        torch.save({'state_dict': self.state_dict()}, path)
        print("Model saved")
        
    def load(self, path):
        cuda = torch.cuda.is_available()
        device = torch.device('cuda' if cuda else 'cpu')
        checkpoint = torch.load(path, map_location=device)
        self.load_state_dict(checkpoint['state_dict'])
        print("Model loaded")

def train(model, dataframe, seq_length=300, batch_size=20, epochs=200, lr=1e-3, save:bool=False):
    model.train()
    train_tensor = torch.FloatTensor(dataframe).view(-1, 1)
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)

    for epoch in range(epochs):
        for i in range(0, len(train_tensor) - seq_length, batch_size):
            optimizer.zero_grad()
            batch_input = train_tensor[i:i+seq_length].view(seq_length, -1, 1)
            batch_output = train_tensor[i+seq_length:i+seq_length+batch_size]
            predictions = model(batch_input)
            loss = criterion(predictions, batch_output)
            loss.backward()
            optimizer.step()

        if epoch % 10 == 0:
            print(f'Epoch {epoch}/{epochs}, Loss {loss.item()}')

    print("Обучение завершено.")
    if save:
        model.save("trained_model.pth")

def savedModelForecast(dataframe_path = "./dataset.csv", path="./trained_model.pth", column="salary", future=100, seq_length=300):
    df = pd.read_csv(dataframe_path)
    df['date'] = pd.to_datetime(df['date'])
    indexedData = df.set_index('date')[column]
    data = indexedData.values
    data_tensor = torch.FloatTensor(data).view(-1, 1)

    model = LSTM()
    model.load("trained_model.pth")

    preds = model.forecast(data_tensor, future=future, sequence_length=seq_length)

    return preds

def trainAndForecast(dataframe_path = "./dataset.csv", path="./trained_model.pth", column="salary", future=100, seq_length=300):
    df = pd.read_csv(dataframe_path)
    df['date'] = pd.to_datetime(df['date'])
    indexedData = df.set_index('date')[column]
    data = indexedData.values
    data_tensor = torch.FloatTensor(data).view(-1, 1)

    model = LSTM()
    model.load("trained_model.pth")
    model.train(data_tensor)

    preds = model.forecast(data_tensor, future=future, sequence_length=seq_length)
    
    return preds

def testTrainingModel(dataframe_path="./dataset.csv", column:str='salary', seq_length:int = 200, batch_size:int=20, epochs:int=120, save:bool=False, load:bool=False, training:bool=True):
    df = pd.read_csv(dataframe_path)
    df.describe()
    df['date'] = pd.to_datetime(df['date'])
    indexedData = df.set_index('date')[column]
    data = indexedData.values

    train_data, test_data = train_test_split(data, test_size=0.2, shuffle=False)

    train_tensor = torch.FloatTensor(train_data).view(-1, 1)
    test_tensor = torch.FloatTensor(test_data).view(-1, 1)

    model = LSTM()
    if load:
        model.load("./trained_model.pth")
    if training:
        train(model, train_data, seq_length, batch_size, epochs, 1e-3, save=True)

    future = len(test_tensor)
    model.eval()

    preds = model.forecast(train_tensor, future=future, sequence_length=seq_length)
    print(len(preds), len(test_data))
    
    mse, mae, mape, corr, r2 = getMetrics(test_data, preds)
    printMetrics(test_data, preds)

    x = np.arange(len(data))
    plt.figure(figsize=(30, 10), dpi=300)
    plt.plot(x, data, color='blue', label='Original Data')
    plt.plot(x[:len(train_data)], train_tensor.reshape(-1), color='red', label='Train Data')
    plt.plot(x[len(train_data):len(train_data)+len(preds)], preds, color='orange', label='Forecast')
    plt.legend()
    plt.title('LSTM Model Forecast')
    fig_dict = fig_to_dict(plt.gcf())
    json_str = json.dumps(fig_dict)
    return json_str

if __name__ == "__main__":
    data = testTrainingModel(column='meantemp', save=False, load=True, training=False)
    plt = json_to_fig(data)
    plt.savefig("test.png", format='png')