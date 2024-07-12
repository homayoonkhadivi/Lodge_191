import streamlit as st
import pandas as pd
from datetime import datetime
import os  # Import the os module for file operations

# File path for storing data
DATA_FILE = "data.csv"

# Function to initialize data storage
def init_data_storage():
    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame(columns=["Name", "Occupation", "Lodge Date", "Comments"])
        df.to_csv(DATA_FILE, index=False)

# Load data from CSV file
def load_data():
    return pd.read_csv(DATA_FILE)

# Function to add a row to the table and save to CSV
def add_row():
    # Format the lodge date as "Month, Year"
    lodge_date = st.session_state.lodge_date.strftime("%B, %Y")
    new_row = pd.DataFrame({
        "Name": [st.session_state.name],
        "Occupation": [st.session_state.occupation],
        "Lodge Date": [lodge_date],
        "Comments": [st.session_state.comments]
    })
    # Append new row to CSV file
    new_row.to_csv(DATA_FILE, mode='a', header=not os.path.exists(DATA_FILE), index=False)
    # Update session state data
    st.session_state.table_data = load_data()

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

# Display the table
st.write("### Current Table")
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
