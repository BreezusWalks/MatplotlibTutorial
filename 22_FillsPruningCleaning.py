import numpy as np
import pickle
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
from matplotlib import style
from mpl_finance import candlestick_ohlc

style.use('ggplot')

def loadSampleStockData():
    with open('stock_data.pickle', 'rb') as pickle_in:
        return pickle.load(pickle_in)

def bytespdate2num(fmt, encoding='utf-8'):
    strconverter = mdates.strpdate2num(fmt)
    def bytesconverter(b):
        s = b.decode(encoding)
        return strconverter(s)
    return bytesconverter

def moving_average(values, window):
    weights = np.repeat(1.0, window)/window
    smas = np.convolve(values, weights, 'valid')
    return smas

def high_minus_low(highs, lows):
    return highs-lows

def graph_data(stock_data):
    fig = plt.figure()
    ax1 = plt.subplot2grid((6,1), (0,0), rowspan=1, colspan=1)
    plt.title('Stock')
    plt.ylabel('H-L')
    ax2 = plt.subplot2grid((6,1), (1,0), rowspan=4, colspan=1)
    plt.ylabel('Price')
    ax3 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1)
    plt.ylabel('MAvgs')

    date, closep, highp, lowp, openp, adj_closep, volume = np.loadtxt(stock_data, delimiter=',', unpack=True, converters={0: bytespdate2num('%Y-%m-%d')})

    x = 0
    y = len(date)
    ohlc = []

    while x < y:
        append_me = date[x], openp[x], highp[x], lowp[x], closep[x], volume[x]
        ohlc.append(append_me)
        x += 1

    ma1 = moving_average(closep, MA1)
    ma2 = moving_average(closep, MA2)
    start = len(date[MA2 - 1:])

    h_l = list(map(high_minus_low, highp, lowp))

    ax1.plot_date(date, h_l, '-')
    ax1.yaxis.set_major_locator(mticker.MaxNLocator(nbins=5, prune='lower'))

    candlestick_ohlc(ax2, ohlc, width=0.4, colorup='#77d879', colordown='#db3f3f')

    bbox_props = dict(boxstyle='round', fc='w', ec='k', lw=1)

    ax2.grid(True)
    ax2.annotate(str(closep[-1]), (date[-1], closep[-1]),
                 xytext=(date[-1] + 4, closep[-1]), bbox=bbox_props)

    ax3.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax3.xaxis.set_major_locator(mticker.MaxNLocator(10))

    ax3.plot(date[-start:], ma1[-start:])
    ax3.plot(date[-start:], ma2[-start:])

    ax3.fill_between(date[-start:], ma2[-start:], ma1[-start:],
                     where=(ma1[-start:] < ma2[-start:]),
                     facecolor='r', edgecolor='r', alpha=0.5)

    ax3.fill_between(date[-start:], ma2[-start:], ma1[-start:],
                     where=(ma1[-start:] > ma2[-start:]),
                     facecolor='g', edgecolor='g', alpha=0.5)

    for label in ax3.xaxis.get_ticklabels():
        label.set_rotation(45)

    plt.setp(ax1.get_xticklabels(), visible=False)
    plt.setp(ax2.get_xticklabels(), visible=False)
    plt.subplots_adjust(left=0.11, bottom=0.24, right=0.90, top=0.90, wspace=0.2, hspace=0)
    plt.show()

MA1 = 10
MA2 = 30

graph_data(loadSampleStockData())