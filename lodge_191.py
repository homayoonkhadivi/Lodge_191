import streamlit as st
import pandas as pd
from datetime import datetime
import os

# File path for storing data (this will only work locally, not on Streamlit sharing)
DATA_FILE = "data.csv"

# Initialize data storage if necessary
def init_data_storage():
    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame(columns=["Name", "Occupation", "Lodge Date", "Grant Date", "Comments"])
        df.to_csv(DATA_FILE, index=False)
    else:
        df = pd.read_csv(DATA_FILE)
        if 'Grant Date' not in df.columns:
            df['Grant Date'] = pd.NaT
            df.to_csv(DATA_FILE, index=False)

# Load data from CSV file with error handling
@st.cache_data
def load_data():
    try:
        if os.path.exists(DATA_FILE):
            df = pd.read_csv(DATA_FILE, parse_dates=['Lodge Date', 'Grant Date'], infer_datetime_format=True)
            return df
        else:
            st.warning(f"No data found in {DATA_FILE}.")
            return pd.DataFrame(columns=["Name", "Occupation", "Lodge Date", "Grant Date", "Comments"])
    except Exception as e:
        st.error(f"Error loading data from {DATA_FILE}: {e}")
        return pd.DataFrame(columns=["Name", "Occupation", "Lodge Date", "Grant Date", "Comments"])

# Function to add a row to the table and save to CSV
def add_row():
    try:
        lodge_date = st.session_state.lodge_date
        grant_date = st.session_state.grant_date
        new_row = pd.DataFrame({
            "Name": [st.session_state.name],
            "Occupation": [st.session_state.occupation],
            "Lodge Date": [lodge_date],
            "Grant Date": [grant_date],
            "Comments": [st.session_state.comments]
        })
        # Append new row to the cached data
        st.session_state.table_data = pd.concat([st.session_state.table_data, new_row], ignore_index=True)
        # Save the updated data to CSV
        st.session_state.table_data.to_csv(DATA_FILE, index=False)
    except Exception as e:
        st.error(f"Error adding row to {DATA_FILE}: {e}")

# Add title with emojis
st.title("191 Lodge List 😊🛂")

# Initialize data storage if necessary
init_data_storage()

# Initialize session state to store table data
if 'table_data' not in st.session_state:
    st.session_state.table_data = load_data()

# Input form for adding new rows
with st.form(key='input_form'):
    st.text_input("Name", key="name")
    st.text_input("Occupation", key="occupation")
    st.date_input("Lodge Date", key="lodge_date", value=datetime.today())
    st.date_input("Grant Date", key="grant_date", value=None)
    st.text_area("Comments", key="comments")
    submit_button = st.form_submit_button(label='Add Row', on_click=add_row)

# Display the table
st.write("### Current Table")
if not st.session_state.table_data.empty:
    # Format Lodge Date to display as "day month year"
    st.session_state.table_data['Lodge Date'] = pd.to_datetime(st.session_state.table_data['Lodge Date'])
    st.session_state.table_data['Lodge Date'] = st.session_state.table_data['Lodge Date'].dt.strftime("%d %B %Y")
    # Show 'None' for Grant Date if it's NaT (not a valid datetime)
    st.session_state.table_data['Grant Date'] = st.session_state.table_data['Grant Date'].apply(lambda x: 'None' if pd.isna(x) else x.strftime("%d %B %Y"))

    # Display the table
    st.dataframe(st.session_state.table_data)

# Function to export table to HTML
def export_to_html():
    html_content = st.session_state.table_data.to_html(index=False)
    st.download_button(
        label="Download Table as HTML",
        data=html_content,
        file_name="table.html",
        mime="text/html"
    )

# Export button
export_to_html()
