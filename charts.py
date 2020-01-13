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

plt.figure(1)
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
plt.savefig("plots/broker_to_consumer_network_traffic.png")

# Consumer Record Throughput

plt.figure(2)
plt.title('Consumer Record Throughput')

metric_name = 'kafka-consumer:records-consumed-total'

y24, y23 = format_series(kafka24[metric_name], kafka23[metric_name])

thousand = 1000

# scale thousands of records
y24 /= thousand
y23 /= thousand

# Add x and y lables, and set their font size
plt.xlabel("time (ms)", fontsize=14)
plt.ylabel("consumed records (x1000)", fontsize=14)

plt.plot(x, y24, **seriesFormatArgs24)
plt.plot(x, y23, **seriesFormatArgs23)

plt.grid()
plt.legend()
plt.savefig("plots/consumer-record-throughput.png")

# Consumer Record Throughput

plt.figure(2)
plt.title('Consumer Record Throughput')

metric_name = 'kafka-consumer:records-consumed-total'

y24, y23 = format_series(kafka24[metric_name], kafka23[metric_name])

thousand = 1000

# scale thousands of records
y24 /= thousand
y23 /= thousand

# Add x and y lables, and set their font size
plt.xlabel("time (ms)", fontsize=14)
plt.ylabel("consumed records (x1000)", fontsize=14)

plt.plot(x, y24, **seriesFormatArgs24)
plt.plot(x, y23, **seriesFormatArgs23)

plt.grid()
plt.legend()
plt.savefig("plots/consumer_record_throughput.png")

# JVM Memory

# plt.figure(3)

metric_jvm_heap_bytes = 'jvm:heap-bytes:mean'
metric_jvm_non_heap_bytes = 'jvm:non-heap-bytes:mean'
metric_jvm_direct_bytes = 'jvm:direct-bytes:mean'

f, (ax_heap, ax_non_heap, ax_direct) = plt.subplots(nrows=1, ncols=3, sharey=False, figsize=(15, 5))

ax_heap.set_title('JVM Heap Memory Usage')

# label left-most sub plot
ax_heap.set_ylabel("bytes used (MB)", fontsize=14)

y24, y23 = format_series(kafka24[metric_jvm_heap_bytes], kafka23[metric_jvm_heap_bytes])

# scale bytes to MB
y24 /= one_mb
y23 /= one_mb

ax_heap.plot(x, y24, **seriesFormatArgs24)
ax_heap.plot(x, y23, **seriesFormatArgs23)

ax_heap.grid()
ax_heap.legend()

ax_non_heap.set_title('JVM Non-Heap Memory Usage')

# label middle sub plot 
ax_non_heap.set_xlabel('time (ms)', fontsize=14)


y24, y23 = format_series(kafka24[metric_jvm_non_heap_bytes], kafka23[metric_jvm_non_heap_bytes])

# scale bytes to MB
y24 /= one_mb
y23 /= one_mb

ax_non_heap.plot(x, y24, **seriesFormatArgs24)
ax_non_heap.plot(x, y23, **seriesFormatArgs23)

ax_non_heap.grid()
ax_non_heap.legend()

ax_direct.set_title('JVM Direct Memory Usage')

y24, y23 = format_series(kafka24[metric_jvm_direct_bytes], kafka23[metric_jvm_direct_bytes])

# scale bytes to MB
y24 /= one_mb
y23 /= one_mb

ax_direct.plot(x, y24, **seriesFormatArgs24)
ax_direct.plot(x, y23, **seriesFormatArgs23)

ax_direct.grid()
ax_direct.legend()

f.savefig("plots/jvm_memory.png")

# Fetch Metrics

metric_fetch_total = 'kafka-consumer:fetch-total'
metric_records_per_fetch_avg = 'kafka-consumer:records-per-request-avg'

f, (ax_fetch_total, ax_records_per_fetch_avg) = plt.subplots(nrows=1, ncols=2, sharey=False, figsize=(10, 5))

ax_fetch_total.set_title('Fetch Requests')

ax_fetch_total.set_ylabel("fetch requests", fontsize=14)
ax_fetch_total.set_xlabel('time (ms)', fontsize=14)

y24, y23 = format_series(kafka24[metric_fetch_total], kafka23[metric_fetch_total])

ax_fetch_total.plot(x, y24, **seriesFormatArgs24)
ax_fetch_total.plot(x, y23, **seriesFormatArgs23)

ax_fetch_total.grid()
ax_fetch_total.legend()

ax_records_per_fetch_avg.set_title('Records per Fetch Request')

ax_records_per_fetch_avg.set_ylabel("records", fontsize=14)
ax_records_per_fetch_avg.set_xlabel('time (ms)', fontsize=14)


# first n records are NaN
# remove first NaN records, format the axis, then re-add NaN when plotting
y24 = kafka24[metric_records_per_fetch_avg]

total_size = len(y24)
non_nan_size = y24.count()
y24_head = y24.head(total_size-non_nan_size)
y24 = y24.tail(non_nan_size)

y23 = kafka23[metric_records_per_fetch_avg]

total_size = len(y23)
non_nan_size = y23.count()
y23_head = y23.head(total_size-non_nan_size)
y23 = y23.tail(non_nan_size)

y24, y23 = format_series(y24, y23)

y24 = y24_head.append(y24)
y23 = y23_head.append(y23)

# y24 had less data so more NaN padding was added during format_series.. truncate it to fix with y23 series
y24 = y24.head(len(y24)-(len(y24)-len(y23)))

ax_records_per_fetch_avg.plot(x, y24, **seriesFormatArgs24)
ax_records_per_fetch_avg.plot(x, y23, **seriesFormatArgs23)

ax_records_per_fetch_avg.grid()
ax_records_per_fetch_avg.legend()

f.savefig("plots/fetch_requests.png")

#plt.show()
