import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mpl_dates


plt.style.use('fivethirtyeight')

data = pd.read_csv('data_time_series.csv')

data['Date'] = pd.to_datetime(data['Date'])

data.sort_values('Date', inplace=True)

price_data = data['Date']
price_close = data['Close']

plt.plot_date(price_data, price_close, linestyle='solid')

plt.gcf().autofmt_xdate()

plt.title('Bitcoin Prices')
plt.xlabel('Date')
plt.ylabel('Closing Price')

plt.tight_layout()
plt.show()