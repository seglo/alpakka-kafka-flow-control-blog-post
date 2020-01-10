# python API refs
# --
# matplotlib.pyplot.plot 	https://matplotlib.org/api/_as_gen/matplotlib.pyplot.plot.html#matplotlib.pyplot.plot
# pd.read_csv				https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html?highlight=read_csv#pandas.read_csv
# pd.Series      			https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.append.html
# pd.DataFrame				https://pandas.pydata.org/pandas-docs/stable/reference/frame.html


import matplotlib.pyplot as plt
import pandas as pd
import numpy as np 
import scipy

from scipy import signal

# https://plot.ly/python/smoothing/#savitzkygolay-filter
def smooth(y):
	return signal.savgol_filter(y, 53, 3)

# append `num` NaN rows to Series
def append_nan(y, num):
	missing_elements = pd.Series([np.nan for i in range(num)])
	return y.append(missing_elements, ignore_index=True)

# format Series for comparison
# 1. Smooth out series for presentation purposes
# 2. Ensure the same dimensionality (same number of rows)
def format_series(y1, y2):
	y1 = pd.Series(smooth(y1))
	y2 = pd.Series(smooth(y2))
	len1 = len(y1)
	len2 = len(y2)
	difference = abs(len1-len2)
	if (len1 > len2):
		y2 = append_nan(y2, difference)
	elif (len2 > len1):
		y1 = append_nan(y1, difference)
	return y1, y2

seriesFormatArgs23 = {'color':'green', 'linewidth':1, 'label':'2.3.1'}
seriesFormatArgs24 = {'color':'blue', 'linewidth':1, 'label':'2.4.0'}

# skip footer, summary line
kafka24 = pd.read_csv('data-kafka240.csv', skipfooter=1)
kafka23 = pd.read_csv('data-kafka231.csv', skipfooter=1)

# must use the `time-ms` of the longer field
# test run before pre-fetch fix will always take longer, so use 2.3.1 results for x axis
x = kafka23['time-ms']

# Broker to Consumer Network Traffic

plt.title('Broker to Consumer Network Traffic')

metric_name = 'broker:kafka.server:type=BrokerTopicMetrics:name=BytesOutPerSec'

y24, y23 = format_series(kafka24[metric_name], kafka23[metric_name])

one_mb = 1000 * 1000

# scale bytes to MB
y24 /= one_mb
y23 /= one_mb

# Add x and y lables, and set their font size
plt.xlabel("time (ms)", fontsize=14)
plt.ylabel("broker bytes out (MB)", fontsize=14)

plt.plot(x, y24, **seriesFormatArgs24)
plt.plot(x, y23, **seriesFormatArgs23)

plt.grid()
plt.legend()
plt.savefig("plots/broker-to-consumer-network-traffic.png")

# 

plt.show()


