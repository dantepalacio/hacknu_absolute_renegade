import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.optim import lr_scheduler
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

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
        if dataframe.shape[0] <= 10:
            return []
        self.eval()
        preds = []
        dataframe_tensor = torch.FloatTensor(dataframe).view(-1, 1)
        test_input = dataframe_tensor[-seq_length:].view(-1, 1)
        with torch.no_grad():
            for i in range(future):
                pred = model(test_input[-seq_length:].view(-1, 1))
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

def train(model, seq_length=300, batch_size=20, epochs=200):
    model.train()
    criterion = nn.MSELoss()
    optimizer = torch.optim.RMSprop(model.parameters(), lr=1e-3)

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
            print(f'Epoch {epoch}/{epochs}, Loss {loss.item()}, Learning Rate {optimizer.get_lr()[0]}')

    print("Обучение завершено.")
    model.save("trained_model.pth")

def savedModelForecast(dataframe_path = "./dataset.csv", path="./trained_model.pth", column="price", future=100, seq_length=300):
    df = pd.read_csv(dataframe_path)
    df['date'] = pd.to_datetime(df['date'])
    indexedData = df.set_index('date')[column]
    data = indexedData.values
    data_tensor = torch.FloatTensor(data).view(-1, 1)

    model = LSTM()
    model.load("trained_model.pth")

    preds = model.forecast(data_tensor, future=future, sequence_length=seq_length)

    return preds

def trainAndForecast(dataframe_path = "./dataset.csv", path="./trained_model.pth", column="price", future=100, seq_length=300):
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

if __name__ == "__main__":
    df = pd.read_csv("./DailyDelhiClimateTrain.csv")
    df.describe()
    df['date'] = pd.to_datetime(df['date'])
    column = 'meantemp'
    indexedData = df.set_index('date')[column]
    data = indexedData.values

    train_data, test_data = train_test_split(data, test_size=0.2, shuffle=False)

    train_tensor = torch.FloatTensor(train_data).view(-1, 1)
    test_tensor = torch.FloatTensor(test_data).view(-1, 1)

    seq_length = len(train_tensor)//4
    batch_size = 20
    epochs = 120

    model = LSTM()
    model.load("trained_model.pth")
    #train(model, seq_length, batch_size, epochs)

    future = len(test_tensor)
    model.eval()

    preds = model.forecast(train_tensor, future=future, sequence_length=seq_length)

    x = np.arange(len(data))
    plt.figure(figsize=(10, 6))
    plt.plot(x, data, color='blue', label='Original Data')
    plt.plot(x[:len(train_data)], train_tensor.reshape(-1), color='red', label='Train Data')
    plt.plot(x[len(train_data):len(train_data)+len(preds)], preds, color='orange', label='Forecast')
    plt.legend()
    plt.title('LSTM Model Forecast')
    plt.show()