# Binypt: A Python Library for Cryptocurrency Data Retrieval and Processing

[![PyPI - Version](https://img.shields.io/pypi/v/binypt-lib?color=pink)](https://github.com/Tejaromalius/Binypt-lib/blob/main/pyproject.toml)
[![PyPI - License](https://img.shields.io/pypi/l/binypt-lib?color=blue)](https://github.com/Tejaromalius/Binypt-lib/blob/main/LICENSE)
[![PyPI - Status](https://img.shields.io/pypi/status/binypt-lib?color=%20%23239b56%20)](https://pypi.org/project/binypt-lib/)

## Overview

**Binypt** is a Python library designed for retrieving historical cryptocurrency price data from the Binance exchange. It allows you to specify trading pairs, time intervals, and date ranges to download and work with historical price data efficiently. This library is a helpful tool for anyone interested in analyzing or visualizing cryptocurrency price trends.

## Features

- Retrieve historical cryptocurrency price data from Binance.
- Specify trading pairs, time intervals, and date ranges.
- Export data in various formats such as CSV, Excel, or Pickle.
- Added human readable dates to the chart.

## Installation

You can install Binypt using `pip`:

```bash
pip install binypt-lib
```

## Usage

Here's a brief overview of how to use Binypt:

```python
from binypt import Binypt

# Initialize Binypt
binypt = Binypt()

# Set data retrieval parameters
binypt.set_arguments("BTCUSDT", "1h", "01/09/2023-00:00:00", "10/09/2023-23:59:59")

# Fetch cryptocurrency price data
binypt.retrieve_data()

# Export data to a CSV file
binypt.export("crypto_data.csv")

# Add human-readable timestamps
binypt.add_human_readable_time()

# Show progress bar and log messages
binypt.set_verbosity(show_bar=True, show_log=True)

# Access the data as a Pandas DataFrame
price_data = binypt.get_data()

# You can now perform various data analysis or visualization tasks with the price_data DataFrame
```

## Contributions

Contributions to this project are welcome. Feel free to submit bug reports, feature requests or pull requests!

## Documentation

To deep dive in on how this library functions, please refer to the [documentation](DOCUMENTATION.md)

---

[![Generated by ChatGPT](https://img.shields.io/badge/Generated%20by-ChatGPT-45b39d.svg)](https://chat.openai.com/)