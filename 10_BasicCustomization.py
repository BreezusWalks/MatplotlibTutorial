import matplotlib.pyplot as plt
import numpy as np
import pickle
import matplotlib.dates as mdates

def loadSampleStockData():
    with open('stock_data.pickle', 'rb') as pickle_in:
        return pickle.load(pickle_in)

def bytespdate2num(fmt, encoding='utf-8'):
    strconverter = mdates.strpdate2num(fmt)
    def bytesconverter(b):
        s = b.decode(encoding)
        return strconverter(s)
    return bytesconverter

def graph_data(stock_data):
    # %Y = full year. 2015
    # %y = partial year 15
    # %m = number month
    # %d = number day
    # %H = hours
    # %M = minutes
    # %S = seconds
    # 12-06-2014
    # %m-%d-%Y
    date, closep, highp, lowp, openp, adj_closep, volume = np.loadtxt(stock_data, delimiter=',', unpack=True, converters={0: bytespdate2num('%Y-%m-%d')})

    fig = plt.figure()
    ax1 = plt.subplot2grid((1,1), (0,0))
    ax1.plot_date(date, closep, '-', label='Price')
    for label in ax1.xaxis.get_ticklabels():
        label.set_rotation(45)
    ax1.grid(True)

    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Interesting Graph\nCheck it out')
    plt.legend()
    plt.subplots_adjust(left=0.09, bottom=0.20, right=0.94, top=0.90, wspace=0.2, hspace=0)
    plt.show()

graph_data(loadSampleStockData())