import requests
import pandas as pd
from datetime import datetime, timedelta
import streamlit as st

FIRE_API_URL = "https://data.lacity.org/resource/3rp3-6znj.json"

st.set_page_config(page_title="LA Fire Incident Tracker", layout="wide")
st.title("\ud83d\udd25 Los Angeles Fire Incident Tracker")

@st.cache_data(show_spinner=False)
def get_fire_data(start_date, end_date):
    query = f"?$where=incident_date between '{start_date}T00:00:00' and '{end_date}T23:59:59'&$limit=50000"
    response = requests.get(FIRE_API_URL + query)
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    else:
        st.error(f"Failed to fetch data: {response.status_code}")
        return pd.DataFrame()

# Sidebar filters
start_date = st.sidebar.date_input("Start Date", datetime.now() - timedelta(days=7))
end_date = st.sidebar.date_input("End Date", datetime.now())

if start_date > end_date:
    st.warning("Start date must be before end date.")
else:
    df = get_fire_data(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
    if not df.empty:
        st.success(f"Showing fire data from {start_date} to {end_date}")
        st.dataframe(df.head(1000))
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("Download CSV", csv, "LA_Fire_Incidents.csv")
    else:
        st.info("No fire incidents found for the selected date range.")
