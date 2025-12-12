import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from app.data.db import connect_database
from app.data.datasets import insert_dataset, get_all_datasets, update_dataset_classification, delete_dataset

def datasets_page():
    if st.button("Back to Home"):
        st.session_state.page = "Home"
        st.rerun()
    st.title("Datasets Management")
    conn = connect_database()

    # Load CSV for statistics
    try:
        datasets_metadata_csv = pd.read_csv('DATA/datasets_metadata.csv')
    except FileNotFoundError:
        st.error("Error loading datasets metadata CSV file.")
        datasets_metadata_csv = pd.DataFrame()

    # CRUD
    tab1, tab2, tab3 = st.tabs(["View/Add", "Update/Delete", "Statistics"])
    
    with tab1:
        st.subheader("Add New Dataset")
        name = st.text_input("Name")
        description = st.text_area("Description")
        source = st.text_input("Source")
        data_type = st.selectbox("Data Type", ["raw", "processed", "aggregated"])
        classification = st.selectbox("Classification", ["public", "internal", "confidential", "restricted"])
        if st.button("Add Dataset"):
            insert_dataset(name, description, source, data_type, classification, st.session_state.user)
            st.success("Dataset added!")
            st.rerun()
    
    with tab2:
        dataset_id = st.number_input("Dataset ID", min_value=1)
        new_classification = st.selectbox("New Classification", ["public", "internal", "confidential", "restricted"])
        if st.button("Update Classification"):
            update_dataset_classification(conn, dataset_id, new_classification)
            st.success("Updated!")
        if st.button("Delete Dataset"):
            delete_dataset(conn, dataset_id)
            st.success("Deleted!")

    with tab3:
        st.subheader("Dataset Statistics")
        if not datasets_metadata_csv.empty:
            col1, col2 = st.columns(2)
            with col1:
                fig1 = px.bar(datasets_metadata_csv, x='uploaded_by', title="Datasets by Uploaded By")
                st.plotly_chart(fig1)
                fig2 = px.pie(datasets_metadata_csv, names='name', values='rows', title="Dataset Sizes (Rows)")
                st.plotly_chart(fig2)
            with col2:
                fig3 = px.bar(datasets_metadata_csv, x='name', y='columns', title="Dataset Columns")
                st.plotly_chart(fig3)
        else:
            st.write("No datasets metadata available.")

    conn.close()
