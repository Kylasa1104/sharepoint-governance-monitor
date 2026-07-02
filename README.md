# sharepoint-governance-monitor
SharePoint Governance Monitoring System using Python, SQL Server, and Power BI for activity auditing, risk detection, and security analytics.
Overview
A data engineering and security analytics project that simulates SharePoint activity, loads audit data into a relational database, detects governance risks, and visualizes security insights in Power BI.
Architecture
log_generator.py
        ↓
CSV Audit Logs

etl_pipeline.py
        ↓
SQL Server / SQLite

governance_rules.py
        ↓
Risk Detection

Power BI Dashboard
Features
Data Generation

Simulated SharePoint audit logs
User activity tracking
Permission assignments

ETL Pipeline

Extract CSV data
Transform and clean records
Load into star schema database

Governance Rules

Mass download detection
Broken inheritance detection
Over-privileged group detection

Dashboard

Insider threat monitoring
Permission exposure analysis
Compliance reporting

Technologies

Python
Pandas
SQLAlchemy
SQL Server
SQLite
Power BI

Database Schema
Fact Table
fact_audit_events

Dimension Tables
dim_users
dim_files
dim_operations
dim_permissions

Running the Project
Generate Audit Logs
python scripts/log_generator.py

Run ETL
python scripts/etl_pipeline.py

Execute Governance Rules
python scripts/governance_rules.py

Power BI
Open:
powerbi/SharePointGovernanceDashboard.pbix

Sample Risks Detected

Insider Threat Activity
Excessive Downloads
Permission Misconfiguration
Overexposed Sensitive Folders
