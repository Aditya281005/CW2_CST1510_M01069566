import streamlit as st
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
    
    # CRUD
    tab1, tab2 = st.tabs(["View/Add", "Update/Delete"])
    
    with tab1:
        st.subheader("All Datasets")
        df = get_all_datasets()
        st.dataframe(df)
        
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
    
    conn.close()
