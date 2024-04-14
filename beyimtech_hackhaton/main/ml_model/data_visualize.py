import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import json

def fig_to_dict(fig):
    fig_dict = {}
    fig_dict['title'] = fig._suptitle.get_text() if fig._suptitle else None

    fig_dict['data'] = []

    for ax in fig.axes:
        ax_dict = {}
        ax_dict['title'] = ax.get_title()
        ax_dict['xlabel'] = ax.get_xlabel()
        ax_dict['ylabel'] = ax.get_ylabel()
        ax_dict['lines'] = []

        for line in ax.get_lines():
            line_dict = {}
            line_dict['label'] = line.get_label()
            line_dict['xdata'] = line.get_xdata().tolist()
            line_dict['ydata'] = line.get_ydata().tolist()
            ax_dict['lines'].append(line_dict)

        fig_dict['data'].append(ax_dict)

    return fig_dict

def fig_to_json(fig):
    fig_dict = fig_to_dict(fig)
    return json.dumps(fig_dict)

def json_to_fig(json_str):
    fig_data = json.loads(json_str)

    fig = plt.figure()

    if fig_data['title']:
        fig.suptitle(fig_data['title'])

    for ax_data in fig_data['data']:
        ax = fig.add_subplot(1, 1, 1)
        ax.set_title(ax_data['title'])
        ax.set_xlabel(ax_data['xlabel'])
        ax.set_ylabel(ax_data['ylabel'])

        for line_data in ax_data['lines']:
            ax.plot(line_data['xdata'], line_data['ydata'], label=line_data['label'])

        ax.legend()

    return fig

def visualizeSingleBoxplot(dataframe, column='salary'):
    plt.figure(figsize=(10, 6))
    sns.boxplot(y='humidity', data=dataframe)
    plt.title(f'Boxplot of {column}')
    plt.ylabel(column)
    plt.tight_layout()
    fig_dict = fig_to_dict(plt.gcf())
    json_str = json.dumps(fig_dict)
    return json_str

def visualizeXYBoxplot(dataframe, by:str, column='salary'):
    plt.figure(figsize=(10, 6))
    sns.boxplot(x = by, y=column, data=dataframe)
    plt.title(f'Boxplot of {by}-{column}')
    plt.xlabel(by)
    plt.ylabel(column)
    plt.xticks(rotation=90, ticks=range(0, len(dataframe[by]), 30))
    plt.tight_layout()
    fig_dict = fig_to_dict(plt.gcf())
    json_str = json.dumps(fig_dict)
    return json_str

def visualizeScatterplot(dataframe, by:str, column='salary'):
    x = dataframe[column].tolist()
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=by, y=column, data=dataframe)
    plt.title(f'Scatterplot of {by}-{column}')
    plt.xlabel(by)
    plt.ylabel(column)
    plt.xticks(rotation=90, ticks=range(0, len(dataframe[by]), 30))
    plt.tight_layout()
    fig_dict = fig_to_dict(plt.gcf())
    json_str = json.dumps(fig_dict)
    return json_str

def visualizeHeatmap(dataframe, columns:list=[]):
    heatmap_data = dataframe[columns]
    plt.figure(figsize=(10, 6))
    sns.heatmap(heatmap_data.corr(), annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Heatmap')
    plt.tight_layout()
    fig_dict = fig_to_dict(plt.gcf())
    json_str = json.dumps(fig_dict)
    return json_str

def visualizeDensity(dataframe, column:str='salary'):
    plt.figure(figsize=(10, 6))
    sns.kdeplot(data=dataframe[column])
    plt.title(f'Density Plot of {column}')
    plt.tight_layout()
    fig_dict = fig_to_dict(plt.gcf())
    json_str = json.dumps(fig_dict)
    return json_str

def visualizeHistplot(dataframe, column:str='salary'):
    plt.figure(figsize=(10, 6))
    sns.histplot(data=dataframe, x=column)
    plt.title(f'Hist Plot of {column}')
    plt.tight_layout()
    fig_dict = fig_to_dict(plt.gcf())
    json_str = json.dumps(fig_dict)
    return json_str

if __name__ == "__main__":
    df = pd.read_csv("./dataset.csv")
    #visualizeSingleBoxplot(df, 'humidity')
    #visualizeXYBoxplot(df, 'wind_speed', 'humidity')
    #visualizeScatterplot(df, 'date', 'humidity')
    #visualizeHeatmap(df, ['humidity', 'meantemp', 'wind_speed'])
    #visualizeDensity(df, 'humidity')
    visualizeHistplot(df, 'wind_speed')
