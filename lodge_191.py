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
            df = pd.read_csv(DATA_FILE)
            # Convert Lodge Date to datetime format if it's not already
            if 'Lodge Date' in df.columns:
                df['Lodge Date'] = pd.to_datetime(df['Lodge Date'], errors='coerce')
                df['Lodge Date'] = df['Lodge Date'].dt.strftime("%d %B, %Y")
            return df
        else:
            st.warning(f"No data found in {DATA_FILE}.")
            return pd.DataFrame(columns=["Name", "Occupation", "Lodge Date", "Comments"])
    except Exception as e:
        st.error(f"Error loading data from {DATA_FILE}: {e}")
        return pd.DataFrame(columns=["Name", "Occupation", "Lodge Date", "Comments"])

# Function to format date with day, month, and year
def format_lodge_date(date):
    return date.strftime("%d %B, %Y")  # Example: "12 July, 2024"

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

# Function to update a row in the table and save to CSV
def update_row(index, updated_row):
    try:
        df = pd.read_csv(DATA_FILE)
        df.loc[index] = updated_row
        df.to_csv(DATA_FILE, index=False)
        st.session_state.table_data = load_data()
    except Exception as e:
        st.error(f"Error updating row in {DATA_FILE}: {e}")

# Add title with emojis
st.title("191 Lodge List 😊🛂")

# Initialize session state to store table data
if 'table_data' not in st.session_state:
    st.session_state.table_data = load_data()

# Input form for adding or updating rows
with st.form(key='input_form'):
    st.text_input("Name", key="name")
    st.text_input("Occupation", key="occupation")
    st.date_input("Lodge Date", key="lodge_date", value=datetime.today())
    st.text_area("Comments", key="comments")
    submit_button = st.form_submit_button(label='Add/Update Row')

    # If a row is selected for editing
    if 'edit_index' in st.session_state:
        st.write("### Editing Row")
        st.write(st.session_state.table_data.loc[st.session_state.edit_index])
        st.session_state.name = st.session_state.table_data.loc[st.session_state.edit_index, 'Name']
        st.session_state.occupation = st.session_state.table_data.loc[st.session_state.edit_index, 'Occupation']
        st.session_state.lodge_date = st.session_state.table_data.loc[st.session_state.edit_index, 'Lodge Date']
        st.session_state.comments = st.session_state.table_data.loc[st.session_state.edit_index, 'Comments']
        if st.button("Clear Edit"):
            del st.session_state['edit_index']
    else:
        if submit_button:
            add_row()

# Display the table with formatted date
st.write("### Current Table")
if not st.session_state.table_data.empty:
    st.dataframe(st.session_state.table_data)

    # Buttons for editing and deleting rows
    st.write("### Actions")
    for index, row in st.session_state.table_data.iterrows():
        if st.button(f"Edit Row {index + 1}"):
            st.session_state.edit_index = index
        if st.button(f"Delete Row {index + 1}"):
            df = pd.read_csv(DATA_FILE)
            df = df.drop(index)
            df.to_csv(DATA_FILE, index=False)
            st.session_state.table_data = load_data()

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
