# project_3_congress_insider
---
# Two Face Assets
This project assesses the purchases and sales of congressmen to verify whether or not their stock trades are factually profitable. Our objective is to investigate the patterns and efficacy of their investment decisions.
## Data Sources
- [Quiver Quantitative's Congressional Trading API](https://www.quiverquant.com/)
- [Yahoo Finance](https://finance.yahoo.com/) (via the `yfinance` Python library)
- [UnitedStates.io](https://www.unitedstates.io/)

## Project Objective
We know that a great many of our leaders don't take office as a wealthy citizen but for those who server long enough, the do end leave office a bit closer the that one percent. Elected officials have capitalized on insider knowledge in the past so it stands to reason that they can and likely are still doing so. What we sought out to find out is if their trades are still profitable and if we can turn a profit trading the same way they do. Using data from the sources mentioned above, we cleaned, merged, and preprocessed the data for our Machine Learning model. Our goal is to find out if political party, committee membership and time in office are factors in their stock purchases or sales. We want to know if their returns are positive or negative on average.

## Data Cleaning and ETL
The two API's that we used to gather our quantitative data, Yahoo Finance and Quiver allowed us to import (2) dataframes to serve as our raw data to clean and process. 
 Yahoo gave us a dataframe that gave the open, high, low, close, adjusted close prices, and volume of all of our 691 stock tickers over the time frame of 3 years, and Quiver gave us a dataframe of congressman’s transactions, the stocks they traded, and the dates that the transactions occurred and were reported.  Using the python libraries pandas, numpy, and datetime, we performed a series of merges, filters, and calculations to create a final dataframe that combined both sources of raw data to give us the financial information (tickers, prices, returns) per transaction per representative.  This final dataframe was then used as the basis for our machine learning model and streamlit UI.

The streamlit UI also gathered legislative data from the UnitedStates.io API to provide background data about the representative chosen by the user.  The raw data was imported in JSON format and had to be parsed and transformed into dataframes to be applicable and presentable on the streamlit UI.

## Setup & Installation

### Jupyter Notebook Dependencies:
For `Full_Congress_Data.ipynb`:
```python
import os
import requests
import json
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from Ticker_Data import og_data
from datetime import datetime
# Machine Learning Dependencies
import xgboost as xgb
import matplotlib.pyplot as plt
from xgboost import plot_importance, plot_tree
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report
from sklearn.ensemble import AdaBoostClassifier
from sklearn import svm
# Plotting Dependencies
import plotly as py
import plotly.io as pio
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
```
For `ticker_data.ipynb`:
```python
import yfinance as yf
```
### Streamlit Application:
To run the Streamlit application, ensure you have the following libraries:
```python
# import shiny as sh (if applicable)
import datetime as dt
import pandas as pd
import requests
import json
```
#### Running Streamlit:

```bash
streamlit run <rep_info>.py
```
## Assumptions and Limitations
### Assumptions:
1. For the Sale Transactions in the Quiver API, since we lack data on when the assets were purchased, we matched the sale transaction date and ticker with the ticker price 30 days prior using `yfinance`, considering congressmen must hold assets for a minimum of 30 days.
2. Our analysis focuses on the timeframe from 2022 onward, bearing in mind the recent congressional elections.
3. During backtesting, we limited our scope to a timeframe the machine learning model was familiar with to avoid introducing unknown factors.
### Limitations:
1. Some stocks were inaccessible due to them being delisted, renamed, or no longer traded. We adjusted our dataset to reflect these changes.
2. The "Purchase" and "Sale" transaction types were imbalanced for the selected period. To address this, we used techniques from the imbalance library.
3. We took a median range for trading volume due to a lack of specific data on the volume of shares traded.
4. Relying on the 30-day prior price for sale transactions resulted in 68 rows with missing pricing data, reducing our dataset's size.
## Dependencies & License
This project hinges on third-party Python libraries (mentioned in the **Setup & Installation** section). Ensure these are installed for seamless execution.
This project operates under the MIT License.
## Support
For assistance or further inquiries:
:e-mail: Contact FabFiveAdvisors LLC at [email@address.com](mailto:email@address.com)








