import streamlit as st
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from app.data.db import connect_database
from app.data.incidents import insert_incident, get_all_incidents, update_incident_status, delete_incident

def incidents_page():
    if st.button("Back to Home"):
        st.session_state.page = "Home"
        st.rerun()
    st.title("Cyber Incidents Management")
    conn = connect_database()
    
    # CRUD
    tab1, tab2 = st.tabs(["View/Add", "Update/Delete"])
    
    with tab1:
        st.subheader("All Incidents")
        df = get_all_incidents()
        st.dataframe(df)
        
        st.subheader("Add New Incident")
        title = st.text_input("Title")
        description = st.text_area("Description")
        incident_date = st.date_input("Date")
        severity = st.selectbox("Severity", ["low", "medium", "high", "critical"])
        status = st.selectbox("Status", ["open", "investigating", "resolved", "closed"])
        if st.button("Add Incident"):
            insert_incident(title, description, str(incident_date), severity, status, None, st.session_state.user)
            st.success("Incident added!")
            st.rerun()
    
    with tab2:
        incident_id = st.number_input("Incident ID", min_value=1)
        new_status = st.selectbox("New Status", ["open", "investigating", "resolved", "closed"])
        if st.button("Update Status"):
            update_incident_status(conn, incident_id, new_status)
            st.success("Updated!")
        if st.button("Delete Incident"):
            delete_incident(conn, incident_id)
            st.success("Deleted!")
    
    conn.close()
