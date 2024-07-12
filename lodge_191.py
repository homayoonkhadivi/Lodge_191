import streamlit as st
import pandas as pd
from datetime import datetime
import os

# File path for storing data
DATA_FILE = "data.csv"

# Function to initialize data storage
def init_data_storage():
    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame(columns=["Name", "Occupation", "Lodge Date", "Comments"])
        df.to_csv(DATA_FILE, index=False)

# Load data from CSV file with error handling
def load_data():
    try:
        if os.path.exists(DATA_FILE):
            return pd.read_csv(DATA_FILE)
        else:
            st.warning(f"No data found in {DATA_FILE}.")
            return pd.DataFrame(columns=["Name", "Occupation", "Lodge Date", "Comments"])
    except Exception as e:
        st.error(f"Error loading data from {DATA_FILE}: {e}")
        return pd.DataFrame(columns=["Name", "Occupation", "Lodge Date", "Comments"])

# Function to format date with day, month, and year
def format_lodge_date(date):
    return date.strftime("%A, %B %d, %Y")  # Example: "Monday, July 12, 2024"

# Function to add a row to the table and save to CSV
def add_row():
    try:
        lodge_date = st.session_state.lodge_date
        formatted_date = format_lodge_date(lodge_date)
        new_row = pd.DataFrame({
            "Name": [st.session_state.name],
            "Occupation": [st.session_state.occupation],
            "Lodge Date": [formatted_date],
            "Comments": [st.session_state.comments]
        })
        # Append new row to CSV file
        new_row.to_csv(DATA_FILE, mode='a', header=not os.path.exists(DATA_FILE), index=False)
        # Update session state data
        st.session_state.table_data = load_data()
    except Exception as e:
        st.error(f"Error adding row to {DATA_FILE}: {e}")

# Add title with emojis
st.title("191 Lodge List 😊🛂")

# Initialize session state to store table data
if 'table_data' not in st.session_state:
    st.session_state.table_data = load_data()

# Input form for adding new rows
with st.form(key='input_form'):
    st.text_input("Name", key="name")
    st.text_input("Occupation", key="occupation")
    st.date_input("Lodge Date", key="lodge_date", value=datetime.today())
    st.text_area("Comments", key="comments")
    submit_button = st.form_submit_button(label='Add Row', on_click=add_row)

# Display the table with formatted date
st.write("### Current Table")
if not st.session_state.table_data.empty:
    st.session_state.table_data['Lodge Date'] = pd.to_datetime(st.session_state.table_data['Lodge Date'])
    st.session_state.table_data['Lodge Date'] = st.session_state.table_data['Lodge Date'].dt.strftime("%A, %B %d, %Y")
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
