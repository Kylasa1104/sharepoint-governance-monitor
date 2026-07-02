 
# log_generator.py

import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

# -------------------------------
# CONFIG
# -------------------------------
NUM_RECORDS = 500
SITE_PATH = "/sites/cyber-incident-response"

OPERATIONS = [
    "FileAccessed",
    "FileSharedExternally",
    "PermissionsModified",
    "FileDownloaded"
]

FILE_TYPES = [".docx", ".xlsx", ".pdf", ".pptx", ".txt", ".py"]

FOLDER_NAMES = [
    "Security_Logs",
    "Topology",
    "Passwords",
    "HR",
    "Finance",
    "Projects",
    "General"
]

PERMISSION_LEVELS = ["Full Control", "Edit", "Read"]
GROUP_NAMES = ["Owners", "Members", "Visitors", "ExternalUsers"]

# -------------------------------
# 1. GENERATE SHAREPOINT AUDIT LOGS
# -------------------------------

audit_records = []

for _ in range(NUM_RECORDS):
    folder = random.choice(FOLDER_NAMES)

    file_name = f"{fake.word().capitalize()}_{random.randint(1,100)}{random.choice(FILE_TYPES)}"

    record = {
        "Timestamp": fake.date_time_between(start_date="-30d", end_date="now"),
        "User_ID": fake.email(),
        "Operation": random.choice(OPERATIONS),
        "Item_Name": file_name,
        "Site_Collection_Path": SITE_PATH
    }

    audit_records.append(record)

audit_df = pd.DataFrame(audit_records)

# -------------------------------
# 2. GENERATE PERMISSIONS MATRIX
# -------------------------------

permissions_records = []

for folder in FOLDER_NAMES:
    for group in GROUP_NAMES:
        permissions_records.append({
            "Folder_Path": f"{SITE_PATH}/{folder.lower()}",
            "Group_Name": group,
            "Permission_Level": random.choice(PERMISSION_LEVELS),
            "Inheritance_Status": random.choice(["Inherited", "Unique"])
        })

permissions_df = pd.DataFrame(permissions_records)

# -------------------------------
# 3. SAVE FILES
# -------------------------------

audit_df.to_csv("sharepoint_audit_events.csv", index=False)
permissions_df.to_csv("site_permissions_matrix.csv", index=False)

print("✅ Files generated successfully!")
print(" - sharepoint_audit_events.csv")
print(" - site_permissions_matrix.csv")