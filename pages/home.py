import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import sys
import os
import requests
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

    # CSV Files Stats
    st.subheader("CSV Files Statistics")
    try:
        incidents_csv = pd.read_csv('DATA/cyber_incidents.csv')
        st.write(f"**Cyber Incidents CSV:** {len(incidents_csv)} rows")
    except FileNotFoundError:
        st.write("**Cyber Incidents CSV:** File not found")

    try:
        datasets_csv = pd.read_csv('DATA/datasets_metadata.csv')
        st.write(f"**Datasets Metadata CSV:** {len(datasets_csv)} rows")
    except FileNotFoundError:
        st.write("**Datasets Metadata CSV:** File not found")

    try:
        tickets_csv = pd.read_csv('DATA/it_tickets.csv')
        st.write(f"**IT Tickets CSV:** {len(tickets_csv)} rows")
    except FileNotFoundError:
        st.write("**IT Tickets CSV:** File not found")

    conn.close()

def chatbot_page():
    """Simple rule-based chatbot for the Intelligence Platform"""
    if st.button("🏠 Back to Home"):
        st.session_state.page = "Home"
        st.rerun()
    
    st.title("🤖 Intelligence Platform Chatbot")
    st.write("Ask me about incidents, datasets, tickets, or platform statistics!")
    
    # Initialize chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
        # Add welcome message
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": f"Hello {st.session_state.user}! 👋 I'm your Intelligence Platform assistant. I can help you with:\n\n• 📊 View statistics\n• 🚨 Check incidents\n• 📁 Browse datasets\n• 🎫 Review tickets\n\nJust ask me anything!"
        })
    
    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    user_input = st.chat_input("Type your message here...")
    
    if user_input:
        # Add user message to history
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input
        })
        
        # Generate bot response
        bot_response = generate_chatbot_response(user_input)
        
        # Add bot response to history
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": bot_response
        })
        
        st.rerun()
    
    # Quick action buttons
    st.sidebar.subheader("Quick Actions")
    
    if st.sidebar.button("📊 Platform Overview"):
        st.session_state.chat_history.append({
            "role": "user",
            "content": "Show me platform overview"
        })
        bot_response = generate_chatbot_response("Show me platform overview")
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": bot_response
        })
        st.rerun()
    
    if st.sidebar.button("🚨 Incident Statistics"):
        st.session_state.chat_history.append({
            "role": "user",
            "content": "Show incident statistics"
        })
        bot_response = generate_chatbot_response("Show incident statistics")
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": bot_response
        })
        st.rerun()
    
    if st.sidebar.button("🎫 Ticket Statistics"):
        st.session_state.chat_history.append({
            "role": "user",
            "content": "Show ticket statistics"
        })
        bot_response = generate_chatbot_response("Show ticket statistics")
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": bot_response
        })
        st.rerun()
    
    if st.sidebar.button("📁 Dataset Statistics"):
        st.session_state.chat_history.append({
            "role": "user",
            "content": "Show dataset statistics"
        })
        bot_response = generate_chatbot_response("Show dataset statistics")
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": bot_response
        })
        st.rerun()
    
    if st.sidebar.button("📈 Performance Metrics"):
        st.session_state.chat_history.append({
            "role": "user",
            "content": "Show performance metrics"
        })
        bot_response = generate_chatbot_response("Show performance metrics")
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": bot_response
        })
        st.rerun()
    
    if st.sidebar.button("⚠️ Severity Analysis"):
        st.session_state.chat_history.append({
            "role": "user",
            "content": "Show severity analysis"
        })
        bot_response = generate_chatbot_response("Show severity analysis")
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": bot_response
        })
        st.rerun()
    
    st.sidebar.divider()
    
    if st.sidebar.button("🧹 Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

def generate_chatbot_response(user_input):
    """Generate responses based on user input with enhanced CSV statistics"""
    user_input_lower = user_input.lower()
    
    try:
        # Import the enhanced statistics service
        sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
        from app.services.chat_statistics import (
            format_statistics_response,
            get_platform_overview,
            get_critical_incidents,
            get_open_tickets,
            get_recent_datasets,
            get_incidents_statistics,
            get_tickets_statistics,
            get_datasets_statistics
        )
        
        # Platform overview / general statistics
        if any(word in user_input_lower for word in ['overview', 'summary', 'platform']):
            return get_platform_overview()
        
        # Detailed incident statistics from CSV
        elif any(word in user_input_lower for word in ['incident statistics', 'incident stats', 'incidents breakdown']):
            return format_statistics_response("incidents")
        
        # General incidents queries
        elif any(word in user_input_lower for word in ['incident', 'incidents', 'security', 'breach', 'cyber']):
            stats = get_incidents_statistics()
            critical_incidents = get_critical_incidents()
            
            response = f"""🚨 **Cyber Incidents Overview**

**Quick Stats:**
• Total Incidents: {stats.get('total', 0)}
• Recent (30 days): {stats.get('recent_count', 'N/A')}

**By Severity:**
"""
            for severity, count in stats.get('by_severity', {}).items():
                percentage = stats.get('severity_percentages', {}).get(severity, 0)
                response += f"• {severity}: {count} ({percentage}%)\n"
            
            response += "\n**By Status:**\n"
            for status, count in stats.get('by_status', {}).items():
                percentage = stats.get('status_percentages', {}).get(status, 0)
                response += f"• {status}: {count} ({percentage}%)\n"
            
            if critical_incidents:
                response += "\n**🔴 Critical/High Severity Incidents:**\n"
                for inc in critical_incidents[:3]:
                    response += f"• ID {inc['id']}: {inc['category']} - {inc['status']}\n"
            
            response += "\n💡 Type 'incident statistics' for detailed breakdown!"
            return response
        
        # Detailed ticket statistics from CSV
        elif any(word in user_input_lower for word in ['ticket statistics', 'ticket stats', 'tickets breakdown', 'resolution time']):
            return format_statistics_response("tickets")
        
        # General tickets queries
        elif any(word in user_input_lower for word in ['ticket', 'tickets', 'support', 'it support']):
            stats = get_tickets_statistics()
            open_tickets = get_open_tickets()
            
            response = f"""🎫 **IT Tickets Overview**

**Quick Stats:**
• Total Tickets: {stats.get('total', 0)}
• Average Resolution: {stats.get('avg_resolution_hours', 'N/A')} hours

**By Priority:**
"""
            for priority, count in stats.get('by_priority', {}).items():
                percentage = stats.get('priority_percentages', {}).get(priority, 0)
                response += f"• {priority}: {count} ({percentage}%)\n"
            
            response += "\n**By Status:**\n"
            for status, count in stats.get('by_status', {}).items():
                percentage = stats.get('status_percentages', {}).get(status, 0)
                response += f"• {status}: {count} ({percentage}%)\n"
            
            if open_tickets:
                response += "\n**📋 Open/In Progress Tickets:**\n"
                for ticket in open_tickets[:3]:
                    response += f"• ID {ticket['id']}: {ticket['priority']} - {ticket['assigned_to']}\n"
            
            response += "\n💡 Type 'ticket statistics' for detailed breakdown!"
            return response
        
        # Detailed dataset statistics from CSV
        elif any(word in user_input_lower for word in ['dataset statistics', 'dataset stats', 'datasets breakdown']):
            return format_statistics_response("datasets")
        
        # General datasets queries
        elif any(word in user_input_lower for word in ['dataset', 'datasets', 'data']):
            stats = get_datasets_statistics()
            recent_datasets = get_recent_datasets()
            
            response = f"""📁 **Datasets Overview**

**Quick Stats:**
• Total Datasets: {stats.get('total', 0)}
• Total Rows: {stats.get('total_rows', 'N/A'):,}
• Average Size: {stats.get('avg_rows', 'N/A'):,} rows

**By Uploader:**
"""
            for uploader, count in stats.get('by_uploader', {}).items():
                response += f"• {uploader}: {count} datasets\n"
            
            if recent_datasets:
                response += "\n**📊 Recent Datasets:**\n"
                for ds in recent_datasets[:3]:
                    response += f"• {ds['name']}: {ds['rows']:,} rows × {ds['columns']} cols\n"
            
            response += "\n💡 Type 'dataset statistics' for detailed breakdown!"
            return response
        
        # Severity analysis
        elif any(word in user_input_lower for word in ['severity', 'critical', 'high priority']):
            stats = get_incidents_statistics()
            critical_incidents = get_critical_incidents()
            
            response = f"""⚠️ **Severity Analysis**

**Incidents by Severity:**
"""
            for severity, count in stats.get('by_severity', {}).items():
                percentage = stats.get('severity_percentages', {}).get(severity, 0)
                response += f"• {severity}: {count} ({percentage}%)\n"
            
            if critical_incidents:
                response += f"\n**🔴 Critical/High Incidents ({len(critical_incidents)}):**\n"
                for inc in critical_incidents[:5]:
                    response += f"• ID {inc['id']}: {inc['category']} - {inc['status']}\n"
            
            return response
        
        # Performance metrics
        elif any(word in user_input_lower for word in ['performance', 'metrics', 'resolution', 'average time']):
            stats = get_tickets_statistics()
            
            response = f"""📈 **Performance Metrics**

**Ticket Resolution Times:**
• Average: {stats.get('avg_resolution_hours', 'N/A')} hours
• Median: {stats.get('median_resolution_hours', 'N/A')} hours
• Fastest: {stats.get('min_resolution_hours', 'N/A')} hours
• Slowest: {stats.get('max_resolution_hours', 'N/A')} hours

**Team Performance:**
"""
            assignee_perf = stats.get('assignee_performance', {})
            for assignee, perf in sorted(assignee_perf.items(), key=lambda x: x[1]['mean'])[:5]:
                response += f"• {assignee}: {perf['mean']} hrs avg ({int(perf['count'])} tickets)\n"
            
            return response
        
        # Trends analysis
        elif any(word in user_input_lower for word in ['trend', 'trends', 'monthly', 'timeline']):
            inc_stats = get_incidents_statistics()
            
            response = "📊 **Trends Analysis**\n\n"
            
            if 'monthly_trend' in inc_stats:
                response += "**Incident Trends (by month):**\n"
                for month, count in sorted(list(inc_stats['monthly_trend'].items())[-6:]):
                    response += f"• {month}: {count} incidents\n"
            
            return response
        
        # Help queries
        elif any(word in user_input_lower for word in ['help', 'what can you do', 'commands']):
            return """🤖 **I can help you with detailed statistics from CSV files:**

**📊 General Queries:**
• "overview" or "summary" - Platform overview
• "statistics" - General statistics

**🚨 Incidents:**
• "incidents" - Quick incident overview
• "incident statistics" - Detailed breakdown
• "severity" - Severity analysis
• "critical incidents" - High priority items

**🎫 Tickets:**
• "tickets" - Quick ticket overview
• "ticket statistics" - Detailed breakdown
• "resolution time" - Performance metrics
• "open tickets" - Current workload

**📁 Datasets:**
• "datasets" - Quick dataset overview
• "dataset statistics" - Detailed breakdown

**📈 Analysis:**
• "trends" - Timeline analysis
• "performance" - Team metrics

Just ask me anything about your data!"""
        
        # Greeting
        elif any(word in user_input_lower for word in ['hello', 'hi', 'hey', 'greetings']):
            return f"Hello {st.session_state.user}! 👋 I can show you detailed statistics from your CSV files. Try asking 'overview' or 'help'!"
        
        # Thank you
        elif any(word in user_input_lower for word in ['thank', 'thanks']):
            return "You're welcome! Let me know if you need more statistics or insights. 😊"
        
        # Default response
        else:
            return """I'm not sure I understand that query. I can provide detailed statistics from your CSV files!

**Try asking:**
• "Show me the overview"
• "Incident statistics"
• "Ticket breakdown"
• "Dataset information"
• "Performance metrics"

Type 'help' to see all available commands."""
    
    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)}. Please try again or contact support."

def home_page():
    st.title(" Welcome to the Intelligence Platform")
    st.write(f"Hello, {st.session_state.user}! 👋")
    
    # Main navigation buttons
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("🚨 Incidents"):
            st.session_state.page = "Incidents"
            st.rerun()
    with col2:
        if st.button("📊 Datasets"):
            st.session_state.page = "Datasets"
            st.rerun()
    with col3:
        if st.button("🎫 Tickets"):
            st.session_state.page = "Tickets"
            st.rerun()
    with col4:
        if st.button("🤖 Chatbot"):
            st.session_state.page = "Chatbot"
            st.rerun()

    # Add graphs
    conn = connect_database()
    incidents_df = get_all_incidents()
    datasets_df = get_all_datasets()
    tickets_df = get_all_tickets()

    conn.close()



def users_page():
    if st.session_state.role != "admin":
        st.error("Access denied. Admin only.")
        return
    
    st.title("Users Management")
    conn = connect_database()
    
    # CRUD
    tab1, tab2 = st.tabs(["View/Add", "Update/Delete"])
    
    with tab1:
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
    st.sidebar.title("🧭 Navigation")
    if not st.session_state.logged_in:
        login_page()
    else:
        st.sidebar.write(f"👤 Logged in as: {st.session_state.user} ({st.session_state.role})")
        if st.sidebar.button("🚪 Logout"):
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
        elif st.session_state.page == "Chatbot":
            chatbot_page()
        else:
            page_options = ["🏠 Home", "📈 Dashboard", "🤖 Chatbot"]
            if st.session_state.page == "Home":
                index = 0
            elif st.session_state.page == "Dashboard":
                index = 1
            elif st.session_state.page == "Chatbot":
                index = 2
            else:
                index = 0
            page = st.sidebar.radio("📍 Go to", page_options, index=index)
            if "Home" in page:
                st.session_state.page = "Home"
                st.rerun()
            elif "Dashboard" in page:
                dashboard_page()
            elif "Chatbot" in page:
                st.session_state.page = "Chatbot"
                st.rerun()

if __name__ == "__main__":
    main()
