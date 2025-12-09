import streamlit as st
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
    
    # CRUD
    tab1, tab2 = st.tabs(["View/Add", "Update/Delete"])
    
    with tab1:
        st.subheader("All Tickets")
        df = get_all_tickets()
        st.dataframe(df)
        
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
    
    conn.close()
