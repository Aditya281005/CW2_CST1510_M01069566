import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from app.data.db import connect_database
from app.data.schema import create_all_tables
from app.services.user_service import register_user, login_user
from app.data.incidents import insert_incident, get_all_incidents, update_incident_status, delete_incident
from app.data.datasets import insert_dataset, get_all_datasets, update_dataset_classification, delete_dataset
from app.data.tickets import insert_ticket, get_all_tickets, update_ticket_status, delete_ticket
from app.data.users import insert_user, get_all_users, update_user_role, delete_user

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user' not in st.session_state:
    st.session_state.user = None
if 'role' not in st.session_state:
    st.session_state.role = None
if 'page' not in st.session_state:
    st.session_state.page = "Home"

# Page functions
def login_page():
    st.title("Login / Register")
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            success, msg = login_user(username, password)
            if success:
                st.session_state.logged_in = True
                st.session_state.user = username
                st.session_state.role = msg.split()[-1]  # Assuming msg includes role
                st.success("Logged in!")
                st.rerun()
            else:
                st.error(msg)
    
    with tab2:
        new_user = st.text_input("Username", key="reg_user")
        new_pass = st.text_input("Password", type="password", key="reg_pass")
        role = st.selectbox("Role", ["user", "analyst", "admin"], key="reg_role")
        if st.button("Register"):
            success, msg = register_user(new_user, new_pass, role)
            if success:
                st.success("Registered! Please login.")
            else:
                st.error(msg)

def dashboard_page():
    st.title("Dashboard")
    conn = connect_database()
    
    # Fetch data
    incidents_df = get_all_incidents()
    datasets_df = get_all_datasets()
    tickets_df = get_all_tickets()
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Incidents", len(incidents_df))
    col2.metric("Total Datasets", len(datasets_df))
    col3.metric("Total Tickets", len(tickets_df))
    col4.metric("Logged-in Users", len(get_all_users()))
    
    # Visualizations
    st.subheader("Incident Analytics (Plotly)")
    if not incidents_df.empty:
        fig1 = px.bar(incidents_df, x='severity', title="Incidents by Severity")
        st.plotly_chart(fig1)
        
        fig2 = px.pie(incidents_df, names='status', title="Incidents by Status")
        st.plotly_chart(fig2)
    
    st.subheader("User Creation Trends (Matplotlib)")
    users_df = get_all_users()
    if not users_df.empty:
        fig, ax = plt.subplots()
        users_df['created_at'] = pd.to_datetime(users_df['created_at'])
        users_df.groupby(users_df['created_at'].dt.date).size().plot(kind='bar', ax=ax)
        ax.set_title("Users Created Over Time")
        st.pyplot(fig)

    st.subheader("Ticket Priorities (Plotly)")
    if not tickets_df.empty:
        fig3 = px.pie(tickets_df, names='priority', title="Tickets by Priority")
        st.plotly_chart(fig3)

    conn.close()

def home_page():
    st.title("Welcome to the Intelligence Platform")
    st.write(f"Hello, {st.session_state.user}!")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Incidents"):
            st.session_state.page = "Incidents"
            st.rerun()
    with col2:
        if st.button("Datasets"):
            st.session_state.page = "Datasets"
            st.rerun()
    with col3:
        if st.button("Tickets"):
            st.session_state.page = "Tickets"
            st.rerun()

    # Add graphs
    conn = connect_database()
    incidents_df = get_all_incidents()
    datasets_df = get_all_datasets()
    tickets_df = get_all_tickets()

    conn.close()

    # CSV Statistics Section
    st.header("📊 CSV Data Statistics & Metrics")

    # Load CSV files
    try:
        cyber_incidents_csv = pd.read_csv('DATA/cyber_incidents.csv')
        datasets_metadata_csv = pd.read_csv('DATA/datasets_metadata.csv')
        it_tickets_csv = pd.read_csv('DATA/it_tickets.csv')
    except FileNotFoundError as e:
        st.error(f"Error loading CSV files: {e}")
        return

    # Cyber Incidents Statistics
    st.subheader("🔒 Cyber Incidents Statistics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Incidents", len(cyber_incidents_csv))
    col2.metric("Unique Categories", cyber_incidents_csv['category'].nunique())
    col3.metric("Critical Incidents", len(cyber_incidents_csv[cyber_incidents_csv['severity'] == 'Critical']))
    col4.metric("Resolved Incidents", len(cyber_incidents_csv[cyber_incidents_csv['status'].isin(['Resolved', 'Closed'])]))

    # Incidents Visualizations
    if not cyber_incidents_csv.empty:
        # Severity distribution
        fig1 = px.bar(cyber_incidents_csv['severity'].value_counts(), title="Incidents by Severity")
        st.plotly_chart(fig1)

        # Category distribution
        fig2 = px.pie(cyber_incidents_csv, names='category', title="Incidents by Category")
        st.plotly_chart(fig2)

        # Status distribution
        fig3 = px.bar(cyber_incidents_csv['status'].value_counts(), title="Incidents by Status")
        st.plotly_chart(fig3)

        # Timeline of incidents
        cyber_incidents_csv['timestamp'] = pd.to_datetime(cyber_incidents_csv['timestamp'])
        cyber_incidents_csv['date'] = cyber_incidents_csv['timestamp'].dt.date
        daily_incidents = cyber_incidents_csv.groupby('date').size().reset_index(name='count')
        fig4 = px.line(daily_incidents, x='date', y='count', title="Incidents Over Time")
        st.plotly_chart(fig4)

    # Datasets Metadata Statistics
    st.subheader("📁 Datasets Metadata Statistics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Datasets", len(datasets_metadata_csv))
    col2.metric("Total Rows", datasets_metadata_csv['rows'].sum())
    col3.metric("Total Columns", datasets_metadata_csv['columns'].sum())
    col4.metric("Avg Rows per Dataset", round(datasets_metadata_csv['rows'].mean(), 1))

    # Datasets Visualizations
    if not datasets_metadata_csv.empty:
        # Rows per dataset
        fig5 = px.bar(datasets_metadata_csv, x='name', y='rows', title="Rows per Dataset")
        st.plotly_chart(fig5)

        # Columns per dataset
        fig6 = px.bar(datasets_metadata_csv, x='name', y='columns', title="Columns per Dataset")
        st.plotly_chart(fig6)

        # Uploaded by distribution
        fig7 = px.pie(datasets_metadata_csv, names='uploaded_by', title="Datasets by Uploader")
        st.plotly_chart(fig7)

    # IT Tickets Statistics
    st.subheader("🎫 IT Tickets Statistics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Tickets", len(it_tickets_csv))
    col2.metric("Resolved Tickets", len(it_tickets_csv[it_tickets_csv['status'] == 'Resolved']))
    col3.metric("Avg Resolution Time", f"{round(it_tickets_csv['resolution_time_hours'].mean(), 1)} hrs")
    col4.metric("Critical Tickets", len(it_tickets_csv[it_tickets_csv['priority'] == 'Critical']))

    # Tickets Visualizations
    if not it_tickets_csv.empty:
        # Priority distribution
        fig8 = px.pie(it_tickets_csv, names='priority', title="Tickets by Priority")
        st.plotly_chart(fig8)

        # Status distribution
        fig9 = px.bar(it_tickets_csv['status'].value_counts(), title="Tickets by Status")
        st.plotly_chart(fig9)

        # Resolution time distribution
        fig10 = px.histogram(it_tickets_csv, x='resolution_time_hours', title="Resolution Time Distribution")
        st.plotly_chart(fig10)

        # Assigned to distribution
        fig11 = px.bar(it_tickets_csv['assigned_to'].value_counts(), title="Tickets by Assignee")
        st.plotly_chart(fig11)

def users_page():
    if st.session_state.role != "admin":
        st.error("Access denied. Admin only.")
        return
    
    st.title("Users Management")
    conn = connect_database()
    
    # CRUD
    tab1, tab2 = st.tabs(["View/Add", "Update/Delete"])
    
    with tab1:
        st.subheader("All Users")
        df = get_all_users()
        st.dataframe(df)
        
        st.subheader("Add New User")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        role = st.selectbox("Role", ["user", "analyst", "admin"])
        if st.button("Add User"):
            success, msg = register_user(username, password, role)
            if success:
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)
    
    with tab2:
        user_id = st.number_input("User ID", min_value=1)
        new_role = st.selectbox("New Role", ["user", "analyst", "admin"])
        if st.button("Update Role"):
            update_user_role(conn, user_id, new_role)
            st.success("Updated!")
        if st.button("Delete User"):
            delete_user(conn, user_id)
            st.success("Deleted!")
    
    conn.close()

# Main app logic
def main():
    st.sidebar.title("Navigation")
    if not st.session_state.logged_in:
        login_page()
    else:
        st.sidebar.write(f"Logged in as: {st.session_state.user} ({st.session_state.role})")
        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.session_state.role = None
            st.session_state.page = "Home"
            st.rerun()

        if st.session_state.page == "Home":
            home_page()
        elif st.session_state.page == "Incidents":
            from pages.incidents import incidents_page
            incidents_page()
        elif st.session_state.page == "Datasets":
            from pages.datasets import datasets_page
            datasets_page()
        elif st.session_state.page == "Tickets":
            from pages.tickets import tickets_page
            tickets_page()
        else:
            page = st.sidebar.radio("Go to", ["Home", "Dashboard", "Users"])
            if page == "Home":
                st.session_state.page = "Home"
                st.rerun()
            elif page == "Dashboard":
                dashboard_page()
            elif page == "Users":
                users_page()

if __name__ == "__main__":
    main()
