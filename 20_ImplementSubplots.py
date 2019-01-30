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

def graph_data(stock_data):
    fig = plt.figure()
    ax1 = plt.subplot2grid((6, 1), (0, 0), rowspan=1, colspan=1)
    ax2 = plt.subplot2grid((6, 1), (1, 0), rowspan=4, colspan=1)
    ax3 = plt.subplot2grid((6, 1), (5, 0), rowspan=1, colspan=1)

    date, closep, highp, lowp, openp, adj_closep, volume = np.loadtxt(stock_data, delimiter=',', unpack=True, converters={0: bytespdate2num('%Y-%m-%d')})

    x = 0
    y = len(date)
    ohlc = []

    while x < y:
        append_me = date[x], openp[x], highp[x], lowp[x], closep[x], volume[x]
        ohlc.append(append_me)
        x += 1

    candlestick_ohlc(ax2, ohlc, width=0.4, colorup='#77d879', colordown='#db3f3f')

    for label in ax2.xaxis.get_ticklabels():
        label.set_rotation(45)

    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax2.xaxis.set_major_locator(mticker.MaxNLocator(10))
    ax2.grid(True)

    bbox_props = dict(boxstyle='round', fc='w', ec='k', lw=1)

    ax2.annotate(str(closep[-1]), (date[-1], closep[-1]),
                 xytext=(date[-1] + 4, closep[-1]), bbox=bbox_props)

    ##    # Annotation example with arrow
    ##    ax1.annotate('Bad News!',(date[11],highp[11]),
    ##                 xytext=(0.8, 0.9), textcoords='axes fraction',
    ##                 arrowprops = dict(facecolor='grey',color='grey'))
    ##
    ##
    ##    # Font dict example
    ##    font_dict = {'family':'serif',
    ##                 'color':'darkred',
    ##                 'size':15}
    ##    # Hard coded text
    ##    ax1.text(date[10], closep[1],'Text Example', fontdict=font_dict)

    plt.title('Stock')
    plt.xlabel('Date')
    plt.ylabel('Price')
    # plt.legend()
    plt.subplots_adjust(left=0.11, bottom=0.24, right=0.87, top=0.90, wspace=0.2, hspace=0)
    plt.show()

graph_data(loadSampleStockData())