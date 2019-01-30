import matplotlib.pyplot as plt
import numpy as np
import pickle
import datetime as dt

def loadSampleStockData():
    with open('stock_data.pickle', 'rb') as pickle_in:
        return pickle.load(pickle_in)

def graph_data(stock_data):
    date, closep, highp, lowp, openp, adj_closep, volume = np.loadtxt(stock_data, delimiter=',', unpack=True)

    #UNIX TIME CONVERSION
    dateconv = np.vectorize(dt.datetime.fromtimestamp)
    date = dateconv(date)

    fig = plt.figure()
    ax1 = plt.subplot2grid((1,1), (0,0))
    ax1.plot_date(date, closep, '-', label='Price')
    for label in ax1.xaxis.get_ticklabels():
        label.set_rotation(45)
    ax1.grid(True, color='g', linestyle='-', linewidth=5)

    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Interesting Graph\nCheck it out')
    plt.legend()
    plt.subplots_adjust(left=0.09, bottom=0.20, right=0.94, top=0.90, wspace=0.2, hspace=0)
    plt.show()

# graph_data(loadSampleStockData())
print("Function does not work since the time stamps being inputted from the hardcoded page are in Y-M-D format. "
      "Did not feel like setting up a quandl.get for the stock and finding it in unix time.")