# project_3_congress_insider
---
# Two Face Assets
This project assesses the purchases and sales of congressmen to verify whether or not their stock trades are factually profitable. Our objective is to investigate the patterns and efficacy of their investment decisions.
## Data Sources
- [Quiver Quantitative's Congressional Trading API](https://www.quiverquant.com/)
- [Yahoo Finance](https://finance.yahoo.com/) (via the `yfinance` Python library)
- [UnitedStates.io](https://www.unitedstates.io/)
## Project Objective
Using data from the sources mentioned above, we clean, merge, and preprocess the data to use in a Machine Learning model. Our goal is to predict if a political party, based on their stock purchases or sales, will return a positive or negative value on average.
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








