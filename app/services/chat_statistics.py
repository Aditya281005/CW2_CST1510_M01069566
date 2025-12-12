"""
Chat Statistics Service
Provides detailed statistical analysis for the chatbot from CSV files
"""
import pandas as pd
import os
from datetime import datetime, timedelta

# Define paths to CSV files
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
INCIDENTS_CSV = os.path.join(BASE_DIR, 'DATA', 'cyber_incidents.csv')
DATASETS_CSV = os.path.join(BASE_DIR, 'DATA', 'datasets_metadata.csv')
TICKETS_CSV = os.path.join(BASE_DIR, 'DATA', 'it_tickets.csv')

def load_csv_safe(filepath):
    """Safely load CSV file with error handling"""
    try:
        if os.path.exists(filepath):
            return pd.read_csv(filepath)
        else:
            return pd.DataFrame()
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return pd.DataFrame()

def get_incidents_statistics():
    """Get comprehensive incident statistics"""
    df = load_csv_safe(INCIDENTS_CSV)
    
    if df.empty:
        return {"error": "No incident data available"}
    
    stats = {
        "total": len(df),
        "by_severity": df['severity'].value_counts().to_dict() if 'severity' in df.columns else {},
        "by_category": df['category'].value_counts().to_dict() if 'category' in df.columns else {},
        "by_status": df['status'].value_counts().to_dict() if 'status' in df.columns else {},
    }
    
    # Calculate percentages
    if stats["by_severity"]:
        stats["severity_percentages"] = {k: round(v/stats["total"]*100, 1) for k, v in stats["by_severity"].items()}
    
    if stats["by_status"]:
        stats["status_percentages"] = {k: round(v/stats["total"]*100, 1) for k, v in stats["by_status"].items()}
    
    # Time-based analysis
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['month'] = df['timestamp'].dt.to_period('M')
        stats["monthly_trend"] = df.groupby('month').size().to_dict()
        
        # Recent incidents (last 30 days)
        thirty_days_ago = datetime.now() - timedelta(days=30)
        recent = df[df['timestamp'] >= thirty_days_ago]
        stats["recent_count"] = len(recent)
    
    return stats

def get_datasets_statistics():
    """Get comprehensive dataset statistics"""
    df = load_csv_safe(DATASETS_CSV)
    
    if df.empty:
        return {"error": "No dataset data available"}
    
    stats = {
        "total": len(df),
        "by_uploader": df['uploaded_by'].value_counts().to_dict() if 'uploaded_by' in df.columns else {},
    }
    
    # Size analysis
    if 'rows' in df.columns:
        stats["total_rows"] = int(df['rows'].sum())
        stats["avg_rows"] = int(df['rows'].mean())
        stats["max_rows"] = int(df['rows'].max())
        stats["min_rows"] = int(df['rows'].min())
    
    if 'columns' in df.columns:
        stats["avg_columns"] = round(df['columns'].mean(), 1)
    
    # Upload trends
    if 'upload_date' in df.columns:
        df['upload_date'] = pd.to_datetime(df['upload_date'])
        df['month'] = df['upload_date'].dt.to_period('M')
        stats["monthly_uploads"] = df.groupby('month').size().to_dict()
    
    return stats

def get_tickets_statistics():
    """Get comprehensive ticket statistics"""
    df = load_csv_safe(TICKETS_CSV)
    
    if df.empty:
        return {"error": "No ticket data available"}
    
    stats = {
        "total": len(df),
        "by_priority": df['priority'].value_counts().to_dict() if 'priority' in df.columns else {},
        "by_status": df['status'].value_counts().to_dict() if 'status' in df.columns else {},
        "by_assigned": df['assigned_to'].value_counts().to_dict() if 'assigned_to' in df.columns else {},
    }
    
    # Calculate percentages
    if stats["by_priority"]:
        stats["priority_percentages"] = {k: round(v/stats["total"]*100, 1) for k, v in stats["by_priority"].items()}
    
    if stats["by_status"]:
        stats["status_percentages"] = {k: round(v/stats["total"]*100, 1) for k, v in stats["by_status"].items()}
    
    # Resolution time analysis
    if 'resolution_time_hours' in df.columns:
        resolved = df[df['resolution_time_hours'].notna()]
        if not resolved.empty:
            stats["avg_resolution_hours"] = round(resolved['resolution_time_hours'].mean(), 1)
            stats["min_resolution_hours"] = int(resolved['resolution_time_hours'].min())
            stats["max_resolution_hours"] = int(resolved['resolution_time_hours'].max())
            stats["median_resolution_hours"] = round(resolved['resolution_time_hours'].median(), 1)
    
    # Performance by assignee
    if 'assigned_to' in df.columns and 'resolution_time_hours' in df.columns:
        assignee_performance = df.groupby('assigned_to')['resolution_time_hours'].agg(['mean', 'count']).round(1)
        stats["assignee_performance"] = assignee_performance.to_dict('index')
    
    return stats

def get_critical_incidents():
    """Get critical/high severity incidents"""
    df = load_csv_safe(INCIDENTS_CSV)
    
    if df.empty or 'severity' not in df.columns:
        return []
    
    critical = df[df['severity'].isin(['Critical', 'High'])].head(10)
    
    incidents = []
    for _, row in critical.iterrows():
        incidents.append({
            "id": row.get('incident_id', 'N/A'),
            "severity": row.get('severity', 'N/A'),
            "category": row.get('category', 'N/A'),
            "status": row.get('status', 'N/A'),
            "description": row.get('description', 'N/A')[:50] + "..." if len(str(row.get('description', ''))) > 50 else row.get('description', 'N/A')
        })
    
    return incidents

def get_open_tickets():
    """Get open/in-progress tickets"""
    df = load_csv_safe(TICKETS_CSV)
    
    if df.empty or 'status' not in df.columns:
        return []
    
    open_tickets = df[df['status'].isin(['Open', 'In Progress'])].head(10)
    
    tickets = []
    for _, row in open_tickets.iterrows():
        tickets.append({
            "id": row.get('ticket_id', 'N/A'),
            "priority": row.get('priority', 'N/A'),
            "status": row.get('status', 'N/A'),
            "assigned_to": row.get('assigned_to', 'N/A'),
            "description": row.get('description', 'N/A')[:50] + "..." if len(str(row.get('description', ''))) > 50 else row.get('description', 'N/A')
        })
    
    return tickets

def get_recent_datasets():
    """Get recently uploaded datasets"""
    df = load_csv_safe(DATASETS_CSV)
    
    if df.empty:
        return []
    
    if 'upload_date' in df.columns:
        df['upload_date'] = pd.to_datetime(df['upload_date'])
        df = df.sort_values('upload_date', ascending=False)
    
    recent = df.head(5)
    
    datasets = []
    for _, row in recent.iterrows():
        datasets.append({
            "id": row.get('dataset_id', 'N/A'),
            "name": row.get('name', 'N/A'),
            "rows": row.get('rows', 'N/A'),
            "columns": row.get('columns', 'N/A'),
            "uploaded_by": row.get('uploaded_by', 'N/A'),
            "upload_date": str(row.get('upload_date', 'N/A'))[:10]
        })
    
    return datasets

def format_statistics_response(stats_type):
    """Format statistics into a readable response"""
    if stats_type == "incidents":
        stats = get_incidents_statistics()
        
        if "error" in stats:
            return stats["error"]
        
        response = f"""📊 **Cyber Incidents Statistics**

**Overview:**
• Total Incidents: {stats['total']}
• Recent (Last 30 days): {stats.get('recent_count', 'N/A')}

**By Severity:**
"""
        for severity, count in stats.get('by_severity', {}).items():
            percentage = stats.get('severity_percentages', {}).get(severity, 0)
            response += f"• {severity}: {count} ({percentage}%)\n"
        
        response += "\n**By Status:**\n"
        for status, count in stats.get('by_status', {}).items():
            percentage = stats.get('status_percentages', {}).get(status, 0)
            response += f"• {status}: {count} ({percentage}%)\n"
        
        response += "\n**By Category:**\n"
        for category, count in sorted(stats.get('by_category', {}).items(), key=lambda x: x[1], reverse=True)[:5]:
            response += f"• {category}: {count}\n"
        
        return response
    
    elif stats_type == "tickets":
        stats = get_tickets_statistics()
        
        if "error" in stats:
            return stats["error"]
        
        response = f"""🎫 **IT Tickets Statistics**

**Overview:**
• Total Tickets: {stats['total']}

**By Priority:**
"""
        for priority, count in stats.get('by_priority', {}).items():
            percentage = stats.get('priority_percentages', {}).get(priority, 0)
            response += f"• {priority}: {count} ({percentage}%)\n"
        
        response += "\n**By Status:**\n"
        for status, count in stats.get('by_status', {}).items():
            percentage = stats.get('status_percentages', {}).get(status, 0)
            response += f"• {status}: {count} ({percentage}%)\n"
        
        if 'avg_resolution_hours' in stats:
            response += f"\n**Resolution Time:**\n"
            response += f"• Average: {stats['avg_resolution_hours']} hours\n"
            response += f"• Median: {stats.get('median_resolution_hours', 'N/A')} hours\n"
            response += f"• Min: {stats.get('min_resolution_hours', 'N/A')} hours\n"
            response += f"• Max: {stats.get('max_resolution_hours', 'N/A')} hours\n"
        
        response += "\n**By Assignee:**\n"
        for assignee, count in sorted(stats.get('by_assigned', {}).items(), key=lambda x: x[1], reverse=True)[:5]:
            response += f"• {assignee}: {count} tickets\n"
        
        return response
    
    elif stats_type == "datasets":
        stats = get_datasets_statistics()
        
        if "error" in stats:
            return stats["error"]
        
        response = f"""📁 **Datasets Statistics**

**Overview:**
• Total Datasets: {stats['total']}
• Total Rows: {stats.get('total_rows', 'N/A'):,}
• Average Rows per Dataset: {stats.get('avg_rows', 'N/A'):,}
• Average Columns: {stats.get('avg_columns', 'N/A')}

**Size Range:**
• Largest Dataset: {stats.get('max_rows', 'N/A'):,} rows
• Smallest Dataset: {stats.get('min_rows', 'N/A'):,} rows

**By Uploader:**
"""
        for uploader, count in stats.get('by_uploader', {}).items():
            response += f"• {uploader}: {count} datasets\n"
        
        return response
    
    return "Statistics type not recognized."

def get_platform_overview():
    """Get complete platform overview"""
    incidents_stats = get_incidents_statistics()
    tickets_stats = get_tickets_statistics()
    datasets_stats = get_datasets_statistics()
    
    response = f"""📊 **Intelligence Platform Overview**

**Cyber Incidents:**
• Total: {incidents_stats.get('total', 0)}
• Critical/High: {incidents_stats.get('by_severity', {}).get('Critical', 0) + incidents_stats.get('by_severity', {}).get('High', 0)}
• Open: {incidents_stats.get('by_status', {}).get('Open', 0)}

**IT Tickets:**
• Total: {tickets_stats.get('total', 0)}
• Critical: {tickets_stats.get('by_priority', {}).get('Critical', 0)}
• Open: {tickets_stats.get('by_status', {}).get('Open', 0)}
• Avg Resolution: {tickets_stats.get('avg_resolution_hours', 'N/A')} hours

**Datasets:**
• Total: {datasets_stats.get('total', 0)}
• Total Rows: {datasets_stats.get('total_rows', 'N/A'):,}
• Avg Size: {datasets_stats.get('avg_rows', 'N/A'):,} rows

Type 'incidents', 'tickets', or 'datasets' for detailed statistics!
"""
    
    return response
