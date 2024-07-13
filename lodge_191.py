import streamlit as st
import pandas as pd
from datetime import datetime
import os

# File path for storing data (this will only work locally, for deployment on Streamlit Cloud, this would need to be changed)
DATA_FILE = "data.csv"

# Function to initialize data storage
def init_data_storage():
    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame(columns=["Name", "Occupation", "Lodge Date", "Grant Date", "Comments"])
        df.to_csv(DATA_FILE, index=False)

# Load data from CSV file
@st.cache_data
def load_data():
    try:
        return pd.read_csv(DATA_FILE)
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
            "Lodge Date": [lodge_date.strftime("%d %B %Y")],
            "Grant Date": [grant_date.strftime("%d %B %Y") if grant_date else None],
            "Comments": [st.session_state.comments]
        })
        # Append new row to CSV file
        if not os.path.exists(DATA_FILE):
            new_row.to_csv(DATA_FILE, index=False)
        else:
            new_row.to_csv(DATA_FILE, mode='a', header=False, index=False)
        # Update session state data
        st.session_state.table_data = load_data()
        st.success("Row added successfully!")
    except Exception as e:
        st.error(f"Error adding row to {DATA_FILE}: {e}")

# Add title with emojis
st.title("191 Lodge List 😊🛂")

# Initialize data storage
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
    # Convert Lodge Date and Grant Date to datetime objects
    st.session_state.table_data['Lodge Date'] = pd.to_datetime(st.session_state.table_data['Lodge Date'], errors='coerce').dt.strftime("%d %B %Y")
    st.session_state.table_data['Grant Date'] = pd.to_datetime(st.session_state.table_data['Grant Date'], errors='coerce').dt.strftime("%d %B %Y")
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
