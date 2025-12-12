import streamlit as st
import pandas as pd
import plotly.express as px
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

    # Load CSV for statistics
    try:
        incidents_csv = pd.read_csv('DATA/cyber_incidents.csv')
        incidents_csv['timestamp'] = pd.to_datetime(incidents_csv['timestamp'])
    except FileNotFoundError:
        st.error("Error loading cyber incidents CSV file.")
        incidents_csv = pd.DataFrame()

    # CRUD
    tab1, tab2, tab3 = st.tabs(["View/Add", "Update/Delete", "Statistics"])

    with tab1:
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

    with tab3:
        st.subheader("Incident Statistics")
        if not incidents_csv.empty:
            col1, col2 = st.columns(2)
            with col1:
                fig1 = px.bar(incidents_csv, x='severity', title="Incidents by Severity")
                st.plotly_chart(fig1)
                fig2 = px.pie(incidents_csv, names='category', title="Incidents by Category")
                st.plotly_chart(fig2)
            with col2:
                incidents_over_time = incidents_csv.groupby(incidents_csv['timestamp'].dt.date).size().reset_index(name='count')
                fig3 = px.line(incidents_over_time, x='timestamp', y='count', title="Incidents Over Time")
                st.plotly_chart(fig3)
                fig4 = px.bar(incidents_csv, x='status', title="Incidents by Status")
                st.plotly_chart(fig4)
        else:
            st.write("No incidents data available.")

    conn.close()
