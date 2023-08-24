import os
import pandas as pd
import numpy.random as rnd
import warnings
import json
import sqlalchemy as sql
import datetime
import yfinance as yf
import numpy as np
import hvplot.pandas
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn import svm
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from pandas.tseries.offsets import DateOffset
from sklearn.metrics import classification_report
warnings.filterwarnings('ignore')
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
from pypfopt.expected_returns import mean_historical_return
from pypfopt.risk_models import CovarianceShrinkage
from pypfopt import objective_functions
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices
#from MCForecastTools import MCSimulation
from bokeh.plotting import figure, output_file
from bokeh.resources import INLINE

# Date range
today = datetime.date.today()
start_date = today - datetime.timedelta(days=365*5) #trading days(252) * amount of years to go back 

start = start_date.strftime("%Y-%m-%d")
end = today.strftime("%Y-%m-%d")

# Tickers of assets
assets = ['NOC', 'F', 'JNJ', 'ZTS', 'VTR', 'MRK', 'MO', 'KO', 'DAR', 'THO',
       'T', 'TMUS', 'APTV', 'PLD', 'COIN', 'ABBV', 'TEL', 'TSN', 'URI',
       'UNH', 'EQR', 'EPRT', 'ESS', 'EVBG', 'ES', 'EXC', 'ADC', 'MOS',
       'EXR', 'MOH', 'MRNA', 'FN', 'FERG', 'KDP', 'KRC', 'SGH', 'AYX',
       'FIS', 'FNF', 'ARE', 'ALEX', 'FCPT', 'KRG', 'KR', 'GTY', 'IOT',
       'GILD', 'RTX', 'KLIC', 'HALO', 'PEAK', 'RLJ', 'HEI-A', 'WPM',
       'MAA', 'SYY', 'WELL', 'TNDM', 'SKT', 'PK', 'TFX', 'ROIC', 'RLAY',
       'RWT', 'RBA', 'VZ', 'KHC', 'PARAA', 'LHX', 'SCHW', 'UBA', 'HST',
       'MELI', 'QDEL', 'HHC', 'UE', 'AAP', 'TMO', 'PSA', 'MMM', 'LBTYA',
       'ICHR', 'IRT', 'MKTX', 'AMCX', 'AMCR', 'CBU', 'LBTYK', 'AMT', 'CB',
       'MTB', 'LVMUY', 'CIEN', 'LSI', 'CNC', 'SR', 'BGNE', 'LMT', 'STT',
       'BELFB', 'IIPR', 'PODD', 'CADE', 'CTRE', 'CFG', 'IFF', 'OGS',
       'INVH', 'BXP', 'NVO', 'IRM', 'TRIP', 'TFC', 'TEAM', 'AVB', 'PD',
       'CAG', 'BMY', 'ADM', 'CHPT', 'BEPC', 'ANET', 'JAZZ', 'CCI', 'CUBE',
       'SHO', 'NXRT', 'PGR', 'JBGS', 'PLTK', 'PHIN', 'SBGI', 'DRH', 'DG',
       'DLTR', 'PECO', 'BFS', 'SBAC', 'PFE', 'CLVT', 'PEB', 'STX', 'PYPL',
       'D', 'SLG', 'EIX', 'USB', 'ENTA', 'EPAM', 'NSA', 'INN', 'UDR',
       'UPS', 'EPR', 'EQIX', 'AVTR', 'YUMC', 'LUMN', 'OLCLY', 'AMADY',
       'BUD', 'ANZGY', 'AON', 'ARGX', 'CJPRY', 'SSREY', 'ARKAY', 'AHKSY',
       'ASHTY', 'ASML', 'ASAZY', 'ALPMY', 'AZN', 'ATLKY', 'AVVIY',
       'AXAHY', 'BAESY', 'BBVA', 'SAN', 'BCS', 'CLLNY', 'BAYRY', 'CZMWY',
       'BDRFY', 'CCOEY', 'BNPQY', 'SWRAY', 'BDNNY', 'CGEMY', 'BXBLY',
       'BNTGY', 'CAJPY', 'BRDCY', 'BTI', 'BTLCY', 'BVVBY', 'BURBY',
       'PRNDY', 'PANDY', 'SCGLY', 'SOBKY', 'SFTBY', 'SKHHY', 'SONVY',
       'SONY', 'SPKKY', 'SSEZY', 'STLA', 'OVCHY', 'OTSKY', 'DNNGY', 'STM',
       'OPHLY', 'OMRNY', 'OLYMY', 'OCDDY', 'NVS', 'ZURVY', 'ZLNDY',
       'NRDBY', 'NRILY', 'NMR', 'NOK', 'NNGRY', 'NDEKY', 'NSANY', 'NTTYY',
       'NTDOY', 'NINOY', 'NJDCY', 'NICE', 'SKFRY', 'SPXCY', 'NEXOY',
       'NCMGY', 'SOMMY', 'YASKY', 'SINGY', 'YARIY', 'YAMHY', 'WPP',
       'WRDLY', 'NTES', 'SBGSY', 'SE', 'SKLTY', 'SKHSY', 'SVNDY', 'SGSOY',
       'SMNNY', 'NSRGY', 'NWG', 'NGG', 'NABZY', 'SHECY', 'NCBDY', 'SGIOY',
       'MRAAY', 'MURGY', 'MTUAY', 'MSADY', 'SSDOY', 'SIEGY', 'MHGVY',
       'SMNEY', 'SXYAY', 'MFG', 'SMMNY', 'SMCAY', 'SNN', 'SMFKY', 'SOAGY',
       'SAP', 'MSLOY', 'MTSFY', 'MUFG', 'MIELY', 'MSSMY', 'SNY', 'SDVKY',
       'SAXPY', 'SALRY', 'SAFRY', 'RPT', 'KKPNY', 'RHHBY', 'RIO', 'WJRYY',
       'VLVLY', 'VWAGY', 'VWAPY', 'RNMBY', 'VOD', 'VCISY', 'RTO', 'RELX',
       'RANJY', 'MGDDY', 'VEOEY', 'VACNY', 'MKKGY', 'MBGYY', 'QBIEY',
       'QABSY', 'PUBGY', 'PRYMY', 'MDIBY', 'MZDAY', 'MKTAY', 'PUK',
       'PROSY', 'MQBKY', 'MTHRY', 'LRLCY', 'LZAGY', 'LOGI', 'LYG',
       'JSGRY', 'BMRRY', 'AMKBY', 'ABBNY', 'AAVMY', 'AHEXY', 'ADDYY',
       'ATEYY', 'LGRDY', 'LSRCY', 'AIQUY', 'KHNGY', 'KUBTY', 'KSRYY',
       'ADRNY', 'KMTUY', 'KNRRY', 'KNBWY', 'KGSPY', 'KGFHY', 'KIM',
       'ADYEY', 'KRYAY', 'UPMMY', 'PPRUY', 'KDDIY', 'AEG', 'ANYYY',
       'AONNY', 'AAGIY', 'EADSY', 'AJINY', 'AKZOY', 'ALC', 'KBCSY',
       'JTKWY', 'UUGRY', 'UOVEY', 'UL', 'UMICY', 'UCBJY', 'UBS', 'JRONY',
       'JAPAY', 'JHX', 'TMICY', 'TT', 'TM', 'TOTDY', 'TRYIY', 'JSAIY',
       'ITTOY', 'ISUZY', 'ISNPY', 'IHG', 'ING', 'IFJPY', 'IFNNY', 'IDEXY',
       'TOELY', 'TKOMY', 'IMBBY', 'ICL', 'IBDRY', 'HSQVY', 'TKAMY',
       'HSBC', 'HOCPY', 'TRUMY', 'TEZNY', 'TCEHY', 'TMSNY', 'TLGPY',
       'TLPFY', 'TEF', 'TTNDY', 'TTDKY', 'TAK', 'TSM', 'SSMXY', 'SYIEY',
       'SCMWY', 'HKXCY', 'HMC', 'HCMLY', 'HTHIY', 'HXGBY', 'HESAY',
       'HEINY', 'HDELY', 'SMTOY', 'SMFG', 'HDB', 'HVRRY', 'HLN', 'GSK',
       'GVDNY', 'GNGBY', 'GMAB', 'GBERY', 'GASNY', 'FJTSY', 'FUJIY',
       'FMS', 'FSUGY', 'FBP', 'ALFVY', 'FRRVY', 'RACE', 'ALLE', 'ALIZY',
       'FRCOY', 'FANUY', 'ESLOY', 'EBKDY', 'ERIC', 'EPOKY', 'SUTNY',
       'ENGIY', 'EDPFY', 'ENLAY', 'DRPRY', 'DQJCY', 'DNBBY', 'DSCSY',
       'DEO', 'DTEGY', 'DHLGY', 'SUHJY', 'DBOEY', 'DB', 'DNTUY', 'STBFY',
       'DNZOY', 'DBSDY', 'DASTY', 'DANOY', 'DWAHY', 'DTRUY', 'DKILY',
       'DSNKY', 'DLICY', 'DFKCY', 'DNPLY', 'CSLLY', 'CRH', 'CRARY',
       'CMSQY', 'CODYY', 'CMWAY', 'CRZBY', 'CLPBY', 'CHEOY', 'CHGCY',
       'SZKMY', 'SVNLY', 'SWDBY', 'VAL', 'OLPX', 'PARA', 'HAL', 'QS',
       'CHX', 'CLF', 'DISH', 'ATUS', 'LCID', 'FTV', 'IR', 'WFAFY', 'AIG',
       'YOU', 'CTSH', 'COLB', 'CONN', 'CSGP', 'CWK', 'CVS', 'DDOG', 'DE',
       'DLR', 'DNB', 'EWBC', 'EDIT', 'ESRT', 'ENPH', 'EL', 'FITB',
       'FCNCA', 'FLO', 'FCEL', 'GM', 'GTLB', 'HQY', 'HRL', 'HUN', 'INSP',
       'IQV', 'JKHY', 'JCI', 'JLL', 'JPM', 'KRTX', 'LC', 'FWONK', 'LNC',
       'LPSN', 'MDGL', 'MRVI', 'VAC', 'MPW', 'MSFT', 'MLKN', 'MRTX',
       'TAP', 'MDLZ', 'NDAQ', 'NTRA', 'NFG', 'NYCB', 'NEM', 'NOV', 'NTNX',
       'NVDA', 'OPEN', 'OUT', 'PLUG', 'QTWO', 'RGA', 'RNG', 'RITM',
       'ROKU', 'SBRA', 'SRPT', 'SHLS', 'SWX', 'SYF', 'TEX', 'TSLA',
       'UGI', 'UAL', 'X', 'UNM', 'VCYT', 'VTRS', 'VNO', 'W', 'WBS', 'WFC',
       'WY', 'WTW', 'ZS', 'BAC', 'AKR', 'ACN', 'AFRM', 'AGNC', 'ALB',
       'AMZN', 'AAT', 'FOLD', 'APO', 'AAPL', 'ARRY', 'CAR', 'AXS', 'BILL',
       'CPT', 'COF', 'CAT', 'GTLS', 'ASXFY', 'BHKLY', 'NTDTY', 'MONOY',
       'GRFS', 'DPSGY', 'CNHI', 'MITEY', 'SKBSY', 'PM',
       'CTLT', 'CPB', 'OHI', 'LLY', 'WM', 'SNOW', 'DAL', 'BLNK', 'PEP',
       'CNP', 'MDT', 'GOOGL', 'ALNY', 'ALLY', 'RIVN', 'MMC', 'ATVI',
       'ABT', 'NFLX', 'CTAS', 'CDNA', 'BRO', 'GMED', 'RJF', 'PEG',
       'SBNY', 'SILK', 'EA', 'HPQ', 'Z', 'WAL', 'KMB', 'SHW', 'K', 'GO',
       'IONS', 'PAYC', 'PACW', 'MKC', 'ELAN', 'EW', 'ISRG', 'INCY',
       'IBRX', 'HPP', 'ATO', 'DEI', 'APPS', 'NLY', 'ED', 'BLK', 'BMRN',
       'BIIB', 'SRE', 'DHR', 'HE', 'CRM', 'SGEN', 'BATRK', 'CEG', 'CF',
       'RUN', 'UNICY', 'ELUXY', 'TOSYY', 'TELNY', 'SGAPY', 'KKOYY',
       'BRK-B', 'VFC', 'UNP', 'TTD', 'SYNH', 'SPWR', 'SWAV', 'SBCF',
       'RBLX', 'PG', 'NEE', 'LIN', 'INTC', 'HZNP', 'FATE', 'ENVX',
       'COST', 'CME', 'CHE', 'CELH', 'AVGO', 'ARWR', 'ABNB',
       'JAPSY', 'PSO']
assets.sort()

# Downloading data
og_data = yf.download(assets, start = start, end = end)
#data = og_data.loc[:,('Adj Close', slice(None))]
#data.columns = assets

#Y = data[assets].pct_change().dropna()
#display(og_data)

#display(start)
#display(end)
#display(Y)