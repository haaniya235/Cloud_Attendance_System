import streamlit as st
import pandas as pd
import plotly.express as px

from firebase_config import db
from style import apply_custom_style
from auth import require_auth

st.set_page_config(
    page_title="Student Profile | Attendify",
    page_icon="👩‍🎓",
    layout="wide"
)

if not require_auth():
    st.stop()

apply_custom_style()

# Page header
st.html("""
<div style="
    padding:25px;
    border-radius:18px;
    background:linear-gradient(120deg,#17152f,#29205c,#153b65);
    border:1px solid rgba(160,140,255,0.3);
    margin-bottom:25px;
">
    <h1 style="color:white;margin:0;">👩‍🎓 Student Profile</h1>
    <p style="color:#c9c5e8;margin:8px 0 0 0;">
        View individual student information and attendance performance.
    </p>
</div>
""")

ATTENDANCE_THRESHOLD = 75

# Fetch registered students
student_docs = db.collection("students").stream()

students = []

for doc in student_docs:
    data = doc.to_dict()

    students.append({
        "Student ID": data.get("student_id", doc.id),
        "Student Name": data.get("student_name", ""),
        "Roll Number": data.get("roll_number", ""),
        "Class": data.get("class", ""),
        "Email": data.get("email", ""),
        "Phone": data.get("phone", "")
    })

if not students:
    st.info("No students registered yet. Please register students first.")
    st.stop()

students_df = pd.DataFrame(students)
students_df = students_df.sort_values("Student Name")

# Student selection
st.subheader("🔍 Select Student")

student_options = students_df["Student ID"].tolist()

selected_id = st.selectbox(
    "Choose a student",
    student_options,
    format_func=lambda sid: (
        students_df.loc[
            students_df["Student ID"] == sid,
            "Student Name"
        ].iloc[0]
        + " ("
        + sid
        + ")"
    )
)

selected_student = students_df[
    students_df["Student ID"] == selected_id
].iloc[0]

st.divider()

# Student information
st.subheader("👤 Student Information")

st.markdown(
    f"""
    <div style="
        padding:22px;
        border-radius:15px;
        background:linear-gradient(120deg,#211c42,#172e4e);
        border:1px solid rgba(160,140,255,0.3);
    ">
        <h2 style="color:white;margin:0 0 15px 0;">
            {selected_student['Student Name']}
        </h2>
        <p style="color:#d4d0ee;margin:7px 0;">
            <b>Student ID:</b> {selected_student['Student ID']}
        </p>
        <p style="color:#d4d0ee;margin:7px 0;">
            <b>Roll Number:</b> {selected_student['Roll Number']}
        </p>
        <p style="color:#d4d0ee;margin:7px 0;">
            <b>Class:</b> {selected_student['Class']}
        </p>
        <p style="color:#d4d0ee;margin:7px 0;">
            <b>Email:</b> {selected_student['Email'] or 'Not provided'}
        </p>
        <p style="color:#d4d0ee;margin:7px 0;">
            <b>Phone:</b> {selected_student['Phone'] or 'Not provided'}
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()

# Fetch attendance records
attendance_docs = db.collection("attendance").where(
    "student_id", "==", selected_id
).stream()

attendance_records = []

for doc in attendance_docs:
    data = doc.to_dict()

    attendance_records.append({
        "Date": data.get("date", ""),
        "Status": str(data.get("status", "")).strip().title()
    })

if not attendance_records:
    st.warning("No attendance records found for this student.")
    st.stop()

attendance_df = pd.DataFrame(attendance_records)

attendance_df = attendance_df[
    attendance_df["Status"].isin(["Present", "Absent"])
].copy()

if attendance_df.empty:
    st.warning("No valid attendance records found for this student.")
    st.stop()

attendance_df["Date"] = pd.to_datetime(
    attendance_df["Date"],
    errors="coerce"
)

attendance_df = attendance_df.dropna(subset=["Date"])
attendance_df = attendance_df.sort_values("Date")

if attendance_df.empty:
    st.warning("No valid attendance dates found.")
    st.stop()

# Calculate attendance
total_classes = len(attendance_df)

present = (attendance_df["Status"] == "Present").sum()
absent = (attendance_df["Status"] == "Absent").sum()

percentage = (
    present / total_classes * 100
    if total_classes > 0 else 0
)

st.subheader("📊 Individual Attendance Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Classes", total_classes)

with col2:
    st.metric("Present", int(present))

with col3:
    st.metric("Absent", int(absent))

with col4:
    st.metric("Attendance", f"{percentage:.2f}%")

# Attendance warning
if percentage < ATTENDANCE_THRESHOLD:
    st.error(
        f"⚠️ Attendance Warning: This student has "
        f"{percentage:.2f}% attendance, which is below 75%."
    )
else:
    st.success(
        f"✓ Satisfactory Attendance: {percentage:.2f}% "
        "is at or above the 75% requirement."
    )

st.divider()

# Individual attendance chart
st.subheader("📈 Attendance Distribution")

chart_data = pd.DataFrame({
    "Status": ["Present", "Absent"],
    "Count": [int(present), int(absent)]
})

col1, col2 = st.columns(2)

with col1:
    fig = px.pie(
        chart_data,
        names="Status",
        values="Count",
        hole=0.55,
        title="Present vs Absent"
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.bar(
        chart_data,
        x="Status",
        y="Count",
        color="Status",
        title="Attendance Count",
        color_discrete_map={
            "Present": "#28C76F",
            "Absent": "#EA5455"
        }
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)

# Date-wise attendance history
st.divider()

st.subheader("📅 Date-wise Attendance History")

history_df = attendance_df.copy()

history_df["Date"] = history_df["Date"].dt.strftime("%d-%m-%Y")

history_df = history_df.rename(
    columns={"Date": "Attendance Date"}
)

history_df = history_df.sort_values(
    "Attendance Date",
    ascending=False
)

st.dataframe(
    history_df,
    use_container_width=True,
    hide_index=True
)

# Download individual report
csv_data = history_df.to_csv(index=False).encode("utf-8-sig")

st.download_button(
    label="📥 Download Student Attendance (CSV)",
    data=csv_data,
    file_name=f"{selected_id}_Attendance_Report.csv",
    mime="text/csv",
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