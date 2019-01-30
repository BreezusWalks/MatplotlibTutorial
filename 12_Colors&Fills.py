import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
import pickle

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
    date, closep, highp, lowp, openp, adj_closep, volume = np.loadtxt(stock_data, delimiter=',', unpack=True, converters={0: bytespdate2num('%Y-%m-%d')})

    fig = plt.figure()
    ax1 = plt.subplot2grid((1,1), (0,0))
    ax1.plot_date(date, closep, '-', label='Price')
    for label in ax1.xaxis.get_ticklabels():
        label.set_rotation(45)

    ax1.plot([], [], linewidth=5, label='loss', color='r', alpha=0.5)
    ax1.plot([], [], linewidth=5, label='gain', color='g', alpha=0.5)
    ax1.fill_between(date, closep, closep[0], where=(closep > closep[0]), facecolor='g', alpha=0.5)
    ax1.fill_between(date, closep, closep[0], where=(closep < closep[0]), facecolor='r', alpha=0.5)

    ax1.grid(True)
    ax1.xaxis.label.set_color('c')
    ax1.yaxis.label.set_color('r')
    ax1.set_yticks([0, 200, 400, 600, 800])


    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Sample Stock')
    plt.legend()
    plt.subplots_adjust(left=0.09, bottom=0.20, right=0.94, top=0.90, wspace=0.2, hspace=0)
    plt.show()

graph_data(loadSampleStockData())