# governance_rules.py

import pandas as pd
from sqlalchemy import create_engine

# Connect to database
engine = create_engine("sqlite:///sharepoint_governance.db")

print("\n🚨 Running Cybersecurity Risk Rules...\n")

# --------------------------------------------------
# 1. Broken Inheritance Risk Tracker
# --------------------------------------------------

query_broken_inheritance = """
SELECT 
    dp.Folder_Path,
    dp.Group_Name,
    dp.Permission_Level,
    dp.Inheritance_Status
FROM dim_permissions dp
WHERE dp.Inheritance_Status = 'Unique'
AND (
    LOWER(dp.Folder_Path) LIKE '%security_logs%' OR
    LOWER(dp.Folder_Path) LIKE '%topology%' OR
    LOWER(dp.Folder_Path) LIKE '%passwords%'
)
"""

broken_inheritance_df = pd.read_sql(query_broken_inheritance, engine)

print("🔴 Broken Inheritance Risks:")
print(broken_inheritance_df)

broken_inheritance_df.to_csv("risk_broken_inheritance.csv", index=False)

# --------------------------------------------------
# 2. Data Mass-Download Alarm
# --------------------------------------------------

query_mass_download = """
SELECT *
FROM (
    SELECT 
        f.Timestamp,
        u.User_ID,
        COUNT(*) OVER (
            PARTITION BY u.User_ID 
            ORDER BY f.Timestamp 
            RANGE BETWEEN 600 PRECEDING AND CURRENT ROW
        ) AS download_count
    FROM fact_audit_events f
    JOIN dim_users u ON f.User_Key = u.User_Key
    JOIN dim_operations o ON f.Operation_Key = o.Operation_Key
    JOIN dim_files df ON f.File_Key = df.File_Key
    WHERE o.Operation = 'FileDownloaded'
) sub
WHERE download_count > 20;
"""

mass_download_df = pd.read_sql(query_mass_download, engine)

print("\n🔴 Data Mass-Download Alerts:")
print(mass_download_df)

mass_download_df.to_csv("risk_mass_download.csv", index=False)

# --------------------------------------------------
# 3. Over-Privileged Group Finder
# --------------------------------------------------

query_overprivileged = """
SELECT 
    dp.Group_Name,
    dp.Permission_Level,
    dp.Folder_Path
FROM dim_permissions dp
LEFT JOIN (
    SELECT DISTINCT df.Folder_Path
    FROM fact_audit_events f
    JOIN dim_files df ON f.File_Key = df.File_Key
    WHERE f.Timestamp >= datetime('now', '-90 days')
) active_folders
ON dp.Folder_Path = active_folders.Folder_Path
WHERE active_folders.Folder_Path IS NULL
AND dp.Permission_Level IN ('Full Control', 'Edit');
"""

overprivileged_df = pd.read_sql(query_overprivileged, engine)

print("\n🔴 Over-Privileged Groups (Inactive):")
print(overprivileged_df)

overprivileged_df.to_csv("risk_overprivileged_groups.csv", index=False)

print("\n✅ Risk analysis completed. CSV files generated.")
 
