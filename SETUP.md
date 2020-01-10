# Use miniconda to manage python installation and required packages.

# Download miniconda
https://docs.conda.io/en/latest/miniconda.html

# Install pandas, matplotlib, scipy
conda install pandas
conda install matplotlib
conda install scipy

# Re-alias python to miniconda python in ~/.zshrc
alias python=~/miniconda3/bin/python

# Run Alpakka Kafka benchmark for each version of Kafka
sbt "benchmarks/it:testOnly *.AlpakkaKafkaPlainConsumer -- -z \"bench with normal messages and one hundred partitions with inflight metrics\""
cp benchmarks/target/alpakka-kafka-plain-consumer-normal-msg-100-partitions-with-inflight-metrics-inflight-metrics-details.csv ~/source/alpakka-kafka-prefetch-blog-post/data-kafka{VERSION}.csv