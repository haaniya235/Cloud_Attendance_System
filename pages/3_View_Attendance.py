import streamlit as st
import pandas as pd
import io
from datetime import datetime

from firebase_config import db
from style import apply_custom_style
from auth import require_auth

# Page configuration
st.set_page_config(
    page_title="View Attendance | Attendify",
    page_icon="📋",
    layout="wide"
)
if not require_auth():
    st.stop()
apply_custom_style()

# Header
st.html("""
<div style="
    padding: 25px;
    border-radius: 18px;
    background: linear-gradient(120deg, #17152f, #29205c, #153b65);
    border: 1px solid rgba(160,140,255,0.3);
    margin-bottom: 25px;
">
    <h1 style="color:white; margin:0;">📋 View Attendance</h1>
    <p style="color:#c9c5e8; margin:8px 0 0 0;">
        Search, filter and download student attendance records.
    </p>
</div>
""")

# Fetch attendance records
attendance_docs = db.collection("attendance").stream()

records = []

for doc in attendance_docs:
    data = doc.to_dict()

    records.append({
        "Student ID": data.get("student_id", ""),
        "Student Name": data.get("student_name", ""),
        "Roll Number": data.get("roll_number", ""),
        "Date": data.get("date", ""),
        "Status": data.get("status", "")
    })

if not records:
    st.info("No attendance records found. Please mark attendance first.")
    st.stop()

df = pd.DataFrame(records)

# Sort records by date
df = df.sort_values(by="Date", ascending=False)

# Summary metrics
total_records = len(df)
present_count = (df["Status"].str.lower() == "present").sum()
absent_count = (df["Status"].str.lower() == "absent").sum()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Records", total_records)

with col2:
    st.metric("Present", int(present_count))

with col3:
    st.metric("Absent", int(absent_count))

st.divider()

# Search and filter
st.subheader("🔍 Search & Filter Records")

col1, col2 = st.columns(2)

with col1:
    search = st.text_input(
        "Search Student",
        placeholder="Enter student name or ID..."
    )

with col2:
    status_filter = st.selectbox(
        "Filter by Status",
        ["All", "Present", "Absent"]
    )

filtered_df = df.copy()

if search:
    filtered_df = filtered_df[
        filtered_df["Student Name"].str.contains(
            search, case=False, na=False
        ) |
        filtered_df["Student ID"].str.contains(
            search, case=False, na=False
        )
    ]

if status_filter != "All":
    filtered_df = filtered_df[
        filtered_df["Status"].str.lower() == status_filter.lower()
    ]

st.caption(f"Showing {len(filtered_df)} attendance records")

# Attendance table
st.subheader("📑 Attendance Records")

st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)

st.divider()

# Download section
st.subheader("📥 Download Attendance Records")

st.caption(
    "Download the records currently displayed above. "
    "Your search and status filters will be applied."
)

col1, col2 = st.columns(2)

# CSV download
csv_data = filtered_df.to_csv(index=False).encode("utf-8-sig")

with col1:
    st.download_button(
        label="📄 Download CSV",
        data=csv_data,
        file_name="Attendify_Attendance_Report.csv",
        mime="text/csv",
        use_container_width=True
    )

# Excel download
excel_buffer = io.BytesIO()

with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
    filtered_df.to_excel(
        writer,
        index=False,
        sheet_name="Attendance Records"
    )

excel_data = excel_buffer.getvalue()

with col2:
    st.download_button(
        label="📊 Download Excel",
        data=excel_data,
        file_name="Attendify_Attendance_Report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

# Footer
st.html("""
<div style="
    text-align:center;
    padding:20px;
    color:#999;
    font-size:13px;
">
    Attendify | Cloud-Based Student Attendance Management System
</div>
""")