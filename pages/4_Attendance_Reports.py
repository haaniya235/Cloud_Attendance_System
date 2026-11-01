import streamlit as st
import pandas as pd
import plotly.express as px

from firebase_config import db
from style import apply_custom_style
from auth import require_auth

st.set_page_config(
    page_title="Attendance Reports | Attendify",
    page_icon="📊",
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
    <h1 style="color:white;margin:0;">📊 Attendance Reports</h1>
    <p style="color:#c9c5e8;margin:8px 0 0 0;">
        Analyse attendance performance and identify students
        who need attendance improvement.
    </p>
</div>
""")

# Attendance threshold
ATTENDANCE_THRESHOLD = 75

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

# Clean data
df["Status"] = df["Status"].astype(str).str.strip().str.title()

df = df[df["Status"].isin(["Present", "Absent"])].copy()

if df.empty:
    st.info("No valid Present or Absent records found.")
    st.stop()

# Calculate overall statistics
total_records = len(df)
present_count = (df["Status"] == "Present").sum()
absent_count = (df["Status"] == "Absent").sum()

overall_percentage = (
    (present_count / total_records) * 100
    if total_records > 0 else 0
)

# Student-wise attendance summary
student_summary = df.groupby(
    ["Student ID", "Student Name", "Roll Number"]
).agg(
    Total_Classes=("Status", "count"),
    Present=("Status", lambda x: (x == "Present").sum()),
    Absent=("Status", lambda x: (x == "Absent").sum())
).reset_index()

student_summary["Attendance Percentage"] = (
    student_summary["Present"] /
    student_summary["Total_Classes"] * 100
).round(2)

# Identify students below 75%
student_summary["Attendance Status"] = student_summary[
    "Attendance Percentage"
].apply(
    lambda x: "Warning - Below 75%"
    if x < ATTENDANCE_THRESHOLD
    else "Satisfactory"
)

# Summary metrics
st.subheader("📌 Overall Attendance Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Records", total_records)

with col2:
    st.metric("Present", int(present_count))

with col3:
    st.metric("Absent", int(absent_count))

with col4:
    st.metric("Overall Attendance", f"{overall_percentage:.2f}%")

st.divider()

# Attendance charts
st.subheader("📈 Attendance Analysis")

col1, col2 = st.columns(2)

with col1:
    attendance_chart = pd.DataFrame({
        "Status": ["Present", "Absent"],
        "Count": [int(present_count), int(absent_count)]
    })

    fig = px.pie(
        attendance_chart,
        names="Status",
        values="Count",
        hole=0.55,
        title="Present vs Absent"
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.bar(
        attendance_chart,
        x="Status",
        y="Count",
        color="Status",
        title="Attendance Overview",
        color_discrete_map={
            "Present": "#28C76F",
            "Absent": "#EA5455"
        }
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)

st.divider()

# Attendance warning system
st.subheader("⚠️ Attendance Warning System")

st.caption(
    "Students with attendance below 75% are identified for attention."
)

warning_students = student_summary[
    student_summary["Attendance Percentage"] < ATTENDANCE_THRESHOLD
].copy()

satisfactory_students = student_summary[
    student_summary["Attendance Percentage"] >= ATTENDANCE_THRESHOLD
].copy()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Students Analysed", len(student_summary))

with col2:
    st.metric(
        "Below 75%",
        len(warning_students),
        delta="Need attention",
        delta_color="inverse"
    )

with col3:
    st.metric(
        "75% or Above",
        len(satisfactory_students)
    )

if not warning_students.empty:
    st.warning(
        f"{len(warning_students)} student(s) have attendance below 75%."
    )

    st.dataframe(
        warning_students[
            [
                "Student ID",
                "Student Name",
                "Roll Number",
                "Total_Classes",
                "Present",
                "Absent",
                "Attendance Percentage"
            ]
        ].sort_values("Attendance Percentage"),
        use_container_width=True,
        hide_index=True
    )
else:
    st.success("All students currently have attendance of 75% or above!")

st.divider()

# Complete student-wise report
st.subheader("👩‍🎓 Student-wise Attendance Report")

display_summary = student_summary.sort_values(
    "Attendance Percentage",
    ascending=True
)

st.dataframe(
    display_summary,
    use_container_width=True,
    hide_index=True
)

# Student percentage chart
st.subheader("📊 Student Attendance Percentage")

fig = px.bar(
    student_summary.sort_values("Attendance Percentage"),
    x="Student Name",
    y="Attendance Percentage",
    color="Attendance Percentage",
    color_continuous_scale=["#EA5455", "#7367F0", "#28C76F"],
    range_color=[0, 100],
    title="Attendance Percentage by Student"
)

fig.add_hline(
    y=ATTENDANCE_THRESHOLD,
    line_dash="dash",
    line_color="#EA5455",
    annotation_text="75% Minimum Attendance"
)

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis_range=[0, 105]
)

st.plotly_chart(fig, use_container_width=True)

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