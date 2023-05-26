# this program is based on the video by NeuralNine who has a very good channel on python tutorials.
# the link is : https://www.youtube.com/watch?v=K2rPr0T17yQ

import math
import datetime as dt

import numpy as np
import yfinance as yf

from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.layouts import row, column
from bokeh.models import TextInput, Button, DatePicker, MultiChoice

# to run with bokeh for plotting you need to go the cl and type:
# > bokeh serve --show main.py

def load_data(ticker1, ticker2, start, end):
    df1 = yf.download(ticker1, start, end)
    df2 = yf.download(ticker2, start, end)

    return df1, df2


def plot_data(data, indicators, sync_axis=None):
    df = data
    gain = df.Close > df.Open
    loss = df.Open > df.Close
    width = 12*60*60*1000

    if sync_axis is not None:
        p = figure(x_axis_type="datetime", 
                   tools="pan,wheel_zoom,box_zoom,reset,save", 
                   width=1000,
                   x_range = sync_axis)
    else:
        p = figure(x_axis_type="datetime", 
                   tools="pan,wheel_zoom,box_zoom,reset,save",
                   width=1000)
        
    p.axis.major_label_orientation = math.pi/4
    p.grid.grid_line_alpha = 0.25
    
    p.segment(df.index, df.High, df.index, df.Low, color = "black")
    
    p.vbar(df.index[gain], width, df.Open[gain], df.Close[gain], fill_color="#00ff00", line_color="#00ff00")
    p.vbar(df.index[loss], width, df.Open[loss], df.Close[loss], fill_color="#ff0000", line_color="#ff0000")
    
    for indicator in indicators:
        if indicator == "30 Day SMA":
            df['SMA30'] = df["Close"].rolling(30).mean()
            p.line(df.index, df.SMA30, color="purple", legend_label="30 Day SMA")
        elif indicator == "10 Day SMA":
            df['SMA10'] = df["Close"].rolling(10).mean()
            p.line(df.index, df.SMA10, color="green", legend_label="10 Day SMA")
        elif indicator == "100 Day SMA":
            df['SMA100'] = df["Close"].rolling(100).mean()
            p.line(df.index, df.SMA100, color="yellow", legend_label="100 Day SMA")
        elif indicator == "Linear Regresion Line":
            par = np.polyfit(range(len(df.index.values)), df.Close.values, 1, full=True)
            slope = par[0][0]
            intercept = par[0][1]
            y_pred = [slope * i + intercept for i in range(len(df.index.values))]
            p.segment(df.index[0], y_pred[0], df.index[-1], y_pred[-1], legend_label="Linear Regresion Line", color="red")
    
        p.legend.location = "top_left"
        p.legend.click_policy = "hide"
    
    return p


def on_button_click(ticker1, ticker2, start, end, indicators):
    df1, df2 = load_data(ticker1, ticker2, start, end)
    p1 = plot_data(df1, indicators)
    p2 = plot_data(df2, indicators, sync_axis=p1.x_range)
    curdoc().clear()
    curdoc().add_root(layout)
    curdoc().add_root(row(p1, p2))
    


stock1_text = TextInput(title='Stock 1')
stock2_text = TextInput(title='Stock 2')

date_picker_from = DatePicker(title="Start Date", 
                              value="2022-01-01", 
                              min_date="2000-01-01", 
                              max_date=dt.datetime.now().strftime("%Y-%m-%d"))
        
date_picker_to = DatePicker(title="End Date", 
                            value="2022-07-30", 
                            min_date="2000-01-01", 
                            max_date=dt.datetime.now().strftime("%Y-%m-%d"))


indicators_choice = MultiChoice(title="Indicators", 
                                options=['100 Day SMA', '10 Day SMA', '30 Day SMA', 'Linear Regresion Line'])


load_button = Button(label = 'Load Data', button_type="success")


load_button.on_click(lambda: on_button_click(stock1_text.value, stock2_text.value, 
                                             date_picker_from.value, date_picker_to.value, 
                                             indicators_choice.value))


layout = column(stock1_text, stock2_text, date_picker_from, date_picker_to, indicators_choice, load_button)


curdoc().clear()
curdoc().add_root(layout)
                     

