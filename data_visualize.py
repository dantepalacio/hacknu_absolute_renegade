import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

def visualizeSingleBoxplot(dataframe, column='salary'):
    plt.figure(figsize=(10, 6))
    sns.boxplot(y='humidity', data=dataframe)
    plt.title(f'Boxplot of {column}')
    plt.ylabel(column)
    plt.tight_layout()
    plt.savefig('single_boxplot.png')

def visualizeXYBoxplot(dataframe, by:str, column='salary'):
    plt.figure(figsize=(10, 6))
    sns.boxplot(x = by, y=column, data=dataframe)
    plt.title(f'Boxplot of {by}-{column}')
    plt.xlabel(by)
    plt.ylabel(column)
    plt.xticks(rotation=90, ticks=range(0, len(dataframe[by]), 30))
    plt.tight_layout()
    plt.savefig('x_y_boxplot.png')

def visualizeScatterplot(dataframe, by:str, column='salary'):
    x = dataframe[column].tolist()
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=by, y=column, data=dataframe)
    plt.title(f'Scatterplot of {by}-{column}')
    plt.xlabel(by)
    plt.ylabel(column)
    plt.xticks(rotation=90, ticks=range(0, len(dataframe[by]), 30))
    plt.tight_layout()
    plt.savefig('scatterplot.png')

def visualizeHeatmap(dataframe, columns:list=[]):
    heatmap_data = dataframe[columns]
    plt.figure(figsize=(10, 6))
    sns.heatmap(heatmap_data.corr(), annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Heatmap')
    plt.tight_layout()
    plt.savefig('heatmap.png')

def visualizeDensity(dataframe, column:str='salary'):
    plt.figure(figsize=(10, 6))
    sns.kdeplot(data=dataframe[column])
    plt.title(f'Density Plot of {column}')
    plt.tight_layout()
    plt.savefig('densityplot.png')
    
if __name__ == "__main__":
    df = pd.read_csv("./dataset.csv")
    #visualizeSingleBoxplot(df, 'humidity')
    #visualizeXYBoxplot(df, 'wind_speed', 'humidity')
    #visualizeScatterplot(df, 'date', 'humidity')
    #visualizeHeatmap(df, ['humidity', 'meantemp', 'wind_speed'])
    visualizeDensity(df, 'humidity')
