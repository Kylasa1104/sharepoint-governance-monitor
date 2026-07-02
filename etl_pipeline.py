# etl_pipeline.py

import pandas as pd
from sqlalchemy import create_engine
import os

# -------------------------------
# 1. EXTRACT
# -------------------------------
audit_file = "sharepoint_audit_events.csv"
permissions_file = "site_permissions_matrix.csv"

audit_df = pd.read_csv(audit_file)
permissions_df = pd.read_csv(permissions_file)

# -------------------------------
# 2. TRANSFORM
# -------------------------------

# Convert Timestamp to datetime
audit_df['Timestamp'] = pd.to_datetime(audit_df['Timestamp'])

# Extract file extension from Item_Name
audit_df['File_Extension'] = audit_df['Item_Name'].str.extract(r'(\.[a-zA-Z0-9]+)$')

# Normalize folder path from Item_Name (simulate structure)
audit_df['Folder_Path'] = audit_df['Site_Collection_Path'] + "/" + audit_df['Item_Name'].str.split("_").str[0]

# Clean permissions matrix (ensure consistent casing)
permissions_df['Folder_Path'] = permissions_df['Folder_Path'].str.strip().str.lower()
audit_df['Folder_Path'] = audit_df['Folder_Path'].str.strip().str.lower()

# -------------------------------
# 3. DATA MODELING (STAR SCHEMA)
# -------------------------------

# DIMENSION: Users
dim_users = audit_df[['User_ID']].drop_duplicates().reset_index(drop=True)
dim_users['User_Key'] = dim_users.index + 1

# DIMENSION: Operations
dim_operations = audit_df[['Operation']].drop_duplicates().reset_index(drop=True)
dim_operations['Operation_Key'] = dim_operations.index + 1

# DIMENSION: Files
dim_files = audit_df[['Item_Name', 'File_Extension', 'Folder_Path']].drop_duplicates().reset_index(drop=True)
dim_files['File_Key'] = dim_files.index + 1

# DIMENSION: Permissions
dim_permissions = permissions_df.copy()
dim_permissions['Permission_Key'] = dim_permissions.index + 1

# FACT TABLE: Audit Events
fact_events = audit_df.merge(dim_users, on='User_ID') \
                      .merge(dim_operations, on='Operation') \
                      .merge(dim_files, on=['Item_Name', 'Folder_Path'])

fact_events = fact_events[['Timestamp', 'User_Key', 'Operation_Key', 'File_Key']]

# -------------------------------
# 4. LOAD INTO SQLITE
# -------------------------------

engine = create_engine("sqlite:///sharepoint_governance.db")

dim_users.to_sql("dim_users", engine, if_exists="replace", index=False)
dim_operations.to_sql("dim_operations", engine, if_exists="replace", index=False)
dim_files.to_sql("dim_files", engine, if_exists="replace", index=False)
dim_permissions.to_sql("dim_permissions", engine, if_exists="replace", index=False)
fact_events.to_sql("fact_audit_events", engine, if_exists="replace", index=False)

print("✅ ETL pipeline completed successfully!")
 
