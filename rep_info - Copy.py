# Representative Information
########################################################################
# This script will provide a front end to display information on 
# the selected Congressman
########################################################################

import streamlit as st
import datetime as dt
import pandas as pd
import requests
import json
import time


# URL of the JSON file
json_url = " https://theunitedstates.io/congress-legislators/committees-current.json"

# Send a GET request to the URL and get the JSON data
response = requests.get(json_url)
data = response.json()

curr_committee_df = pd.DataFrame(data)

#Cleanup unecessary columns
curr_committee_df.drop(['minority_url', 'rss_url', 'minority_rss_url', 'house_committee_id', 'subcommittees', 'jurisdiction_source', 'senate_committee_id', 'wikipedia', 'youtube_id'], axis=1, inplace=True)

# URL of the JSON file
json_url = "https://theunitedstates.io/congress-legislators/committee-membership-current.json"

# Send a GET request to the URL and get the JSON data
response = requests.get(json_url)
data = response.json()


# Create a list from the JSON data for each committee and then create a dataframe from the list
for key in data.keys():
    df = pd.DataFrame(data[key])


# merge all the dataframes into one
merged_df = pd.concat([pd.DataFrame(data[key]) for key in data.keys()], keys=data.keys())

#reset index to thomas_id
merged_df.reset_index(inplace=True)


#remaname level_0 to thomas_id
merged_df.rename(columns={'level_0':'thomas_id'}, inplace=True)
#drop level_1
merged_df.drop(['level_1', 'chamber', 'bioguide'], axis=1, inplace=True)

#merge the current committee dataframe with the merged_df dataframe
merged_committee_df = pd.merge(curr_committee_df, merged_df, on="thomas_id", how="outer")
merged_committee_df.rename(columns={'name_x':'committee'}, inplace=True)
merged_committee_df.rename(columns={'name_y':'member_name'}, inplace=True)
merged_committee_df.dropna(subset=['committee'], inplace=True)

#Get a unique list of members
list_members = merged_committee_df['member_name'].unique()
#list_members

#Get legislators bio data
json_url = "https://theunitedstates.io/congress-legislators/legislators-current.json"

# Send a GET request to the URL and get the JSON data
response = requests.get(json_url)
data = response.json()

served_terms = {} # key, senator value start end?
for cg in data: # data list
    for term in cg["terms"]:
        if cg["name"]["official_full"] not in served_terms:
            served_terms[cg["name"]["official_full"]] = {"start": term["start"], "end": term["end"]}
        elif cg["name"]["official_full"] in served_terms:
            served_terms[cg["name"]["official_full"]]["end"] = term['end']

# Adds the cache decorator for Streamlit
@st.cache(allow_output_mutation=True)
def setup():
    print("What does your Congressman do?")
    
st.markdown("# Congress member info")
st.markdown("## Lookup Committee details for Congressman who trade in the markets")

page_bg_img = '''
<style>
body {
background-image: url("https://images.unsplash.com/photo-1520525003249-2b9cdda513bc?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2670&q=80");
background-size: cover;
}
</style>'''

st.markdown(page_bg_img, unsafe_allow_html=True)

congressman = st.selectbox(label= "Select a Congressman", options= list_members)

if st.button("Get Info"):
    if congressman in served_terms:
        st.header(congressman)
        st.write("First term start: ", served_terms[congressman]["start"])
        st.write("Last/Current term end: ", served_terms[congressman]["end"])
        member_committees = merged_committee_df.loc[merged_committee_df['member_name'] == congressman]
        st.dataframe(member_committees)
        st.info('I wonder how much they :moneybag: made with committee knowledge?')
        time.sleep(.5)
        st.info('hhhmmmm :grey_question:')
        st.info('hhhmmmm :grey_question:')
        st.info('hhhmmmm :grey_question:')
        st.info('hhhmmmm :grey_question:')
        time.sleep(.5)
        st.info(':no_mouth:')
                                                
