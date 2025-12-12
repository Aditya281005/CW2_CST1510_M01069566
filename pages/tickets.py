import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from app.data.db import connect_database
from app.data.tickets import insert_ticket, get_all_tickets, update_ticket_status, delete_ticket

def tickets_page():
    if st.button("Back to Home"):
        st.session_state.page = "Home"
        st.rerun()
    st.title("IT Tickets Management")
    conn = connect_database()

    # Load CSV for statistics
    try:
        tickets_csv = pd.read_csv('DATA/it_tickets.csv')
        tickets_csv['created_at'] = pd.to_datetime(tickets_csv['created_at'])
    except FileNotFoundError:
        st.error("Error loading IT tickets CSV file.")
        tickets_csv = pd.DataFrame()

    # CRUD
    tab1, tab2, tab3 = st.tabs(["View/Add", "Update/Delete", "Statistics"])
    
    with tab1:
        st.subheader("Add New Ticket")
        title = st.text_input("Title")
        description = st.text_area("Description")
        priority = st.selectbox("Priority", ["low", "medium", "high", "urgent"])
        category = st.text_input("Category")
        if st.button("Add Ticket"):
            insert_ticket(title, description, priority, "open", category, st.session_state.user)
            st.success("Ticket added!")
            st.rerun()
    
    with tab2:
        ticket_id = st.number_input("Ticket ID", min_value=1)
        new_status = st.selectbox("New Status", ["open", "in_progress", "resolved", "closed"])
        if st.button("Update Status"):
            update_ticket_status(conn, ticket_id, new_status)
            st.success("Updated!")
        if st.button("Delete Ticket"):
            delete_ticket(conn, ticket_id)
            st.success("Deleted!")

    with tab3:
        st.subheader("Ticket Statistics")
        if not tickets_csv.empty:
            col1, col2 = st.columns(2)
            with col1:
                fig1 = px.bar(tickets_csv, x='priority', title="Tickets by Priority")
                st.plotly_chart(fig1)
                fig2 = px.pie(tickets_csv, names='status', title="Tickets by Status")
                st.plotly_chart(fig2)
            with col2:
                tickets_over_time = tickets_csv.groupby(tickets_csv['created_at'].dt.date).size().reset_index(name='count')
                fig3 = px.line(tickets_over_time, x='created_at', y='count', title="Tickets Over Time")
                st.plotly_chart(fig3)
                fig4 = px.bar(tickets_csv, x='assigned_to', title="Tickets by Assigned To")
                st.plotly_chart(fig4)
        else:
            st.write("No tickets data available.")

    conn.close()
