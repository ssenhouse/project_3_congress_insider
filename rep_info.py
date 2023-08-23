# Representative Information
########################################################################
# This script will provide a front end to display information on 
# the selected Congressman
########################################################################

import streamlit as st
import datetime as dt
import pandas as pd
import requests


curr_committe_df= pd.read_json('committee-current.json')

print(curr_committe_df.head())

