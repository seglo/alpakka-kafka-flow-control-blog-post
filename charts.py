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
	print("y: " + str(y) + ", num: " + str(num))
	missing_elements = pd.Series([np.nan for i in range(num)])
	return y.append(missing_elements, ignore_index=True)

# format Series for comparison
# 1. Smooth out series
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

kafka240 = pd.read_csv('data-kafka240.csv')
kafka231 = pd.read_csv('data-kafka231.csv')

# must use the `time-ms` of the longer field
# test run before pre-fetch fix will always take longer, so use 2.3.1 results for x axis
x = kafka231['time-ms']

# Broker to Consumer Network Traffic

plt.title('Broker to Consumer Network Traffic')

metric_name = 'broker:kafka.server:type=BrokerTopicMetrics-name=BytesOutPerSec'

y240, y231 = format_series(kafka240[metric_name], kafka231[metric_name])

# Add x and y lables, and set their font size
plt.xlabel("time (ms)", fontsize=14)
plt.ylabel("broker bytes out (KB)", fontsize=14)

plt.plot(x, y240, color='blue', linewidth=1, label='2.4.0')
plt.plot(x, y231, color='green', linewidth=1, label='2.3.1')

# print(smooth(y231))

plt.grid()
plt.legend()
plt.show()

#print(kafka240)
