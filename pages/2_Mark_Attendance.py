import streamlit as st
from firebase_config import db
from style import apply_custom_style
from datetime import date
from auth import require_auth

# ---------------- PAGE CONFIGURATION ----------------

st.set_page_config(
    page_title="Mark Attendance",
    page_icon="📋",
    layout="wide"
)
if not require_auth():
    st.stop()
apply_custom_style()

# ---------------- BUTTON STYLING ----------------

st.html("""
<style>
/* Present buttons */
div[data-testid="stButton"]:has(button[kind="primary"]) button {
    background: linear-gradient(135deg, #087F5B, #16A36A);
    color: white;
    border: 1px solid #31C48D;
    border-radius: 10px;
    font-weight: 700;
}

/* Absent buttons */
div[data-testid="stButton"]:has(button[kind="secondary"]) button {
    background: linear-gradient(135deg, #A82942, #D13E55);
    color: white;
    border: 1px solid #F16B7D;
    border-radius: 10px;
    font-weight: 700;
}

/* Button hover */
div[data-testid="stButton"] button:hover {
    filter: brightness(1.15);
    border-color: white;
}
</style>
""")

# ---------------- PAGE HEADER ----------------

st.html("""
<div style="
    background: linear-gradient(120deg, #17132f, #211449, #10264a);
    border: 1px solid #55418b;
    border-radius: 20px;
    padding: 30px;
    margin-bottom: 25px;
    box-shadow: 0 0 25px rgba(125, 65, 255, 0.16);
">
    <div style="
        color: #bd9aff;
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 2px;
        margin-bottom: 10px;
    ">ATTENDIFY • BULK ATTENDANCE</div>

    <div style="
        color: white;
        font-size: 30px;
        font-weight: 750;
        margin-bottom: 8px;
    ">📋 Mark Class Attendance</div>

    <div style="
        color: #c2bfd8;
        font-size: 15px;
    ">
        Mark attendance for the entire class using the Present
        and Absent buttons beside each student's name.
    </div>
</div>
""")

# ---------------- DATE SELECTION ----------------

st.markdown("### ✨ Attendance Details")

attendance_date = st.date_input(
    "📅 Select Attendance Date",
    value=date.today()
)

date_key = attendance_date.isoformat()

# ---------------- FETCH STUDENTS ----------------

try:

    students_ref = db.collection("students").stream()
    students = []

    for student in students_ref:

        data = student.to_dict()

        students.append({
            "id": student.id,
            "name": data.get("student_name", "Unknown"),
            "roll": data.get("roll_number", "")
        })

    if not students:

        st.warning(
            "No students registered yet. Please register students first."
        )

    else:

        students.sort(key=lambda x: x["roll"])

        st.markdown("### 🎓 Student Attendance List")

        st.caption(
            "Click the green Present or red Absent button beside each student."
        )

        # ---------------- INITIALIZE STUDENT STATUS ----------------

        for student in students:

            student_id = student["id"]

            status_key = f"status_{date_key}_{student_id}"

            if status_key not in st.session_state:

                record_id = f"{student_id}_{date_key}"

                existing_record = db.collection(
                    "attendance"
                ).document(record_id).get()

                if existing_record.exists:
                    saved_status = existing_record.to_dict().get(
                        "status", "Not Marked"
                    )
                else:
                    saved_status = "Not Marked"

                st.session_state[status_key] = saved_status

        # ---------------- STUDENT LIST ----------------

        for index, student in enumerate(students):

            student_id = student["id"]
            status_key = f"status_{date_key}_{student_id}"

            current_status = st.session_state[status_key]

            st.markdown(
                """
                <div style="
                    border: 1px solid #393254;
                    border-radius: 12px;
                    padding: 12px 15px;
                    margin-top: 7px;
                    background: rgba(35, 29, 65, 0.45);
                ">
                """,
                unsafe_allow_html=True
            )

            name_col, present_col, absent_col = st.columns(
                [3, 1.2, 1.2],
                vertical_alignment="center"
            )

            with name_col:

                st.markdown(
                    f"""
                    **{student['name']}**

                    <span style="color:#aaa2c7;font-size:12px;">
                    Roll: {student['roll']} &nbsp;|&nbsp; ID: {student_id}
                    </span>
                    """,
                    unsafe_allow_html=True
                )

                if current_status == "Present":
                    st.markdown(
                        "<span style='color:#35D69B;font-size:12px;'>"
                        "● PRESENT SELECTED</span>",
                        unsafe_allow_html=True
                    )

                elif current_status == "Absent":
                    st.markdown(
                        "<span style='color:#FF7185;font-size:12px;'>"
                        "● ABSENT SELECTED</span>",
                        unsafe_allow_html=True
                    )

                else:
                    st.caption("Not marked yet")

            with present_col:

                if st.button(
                    "🟢 Present",
                    key=f"present_{date_key}_{student_id}",
                    use_container_width=True,
                    type="primary"
                ):
                    st.session_state[status_key] = "Present"

                    st.rerun()

            with absent_col:

                if st.button(
                    "🔴 Absent",
                    key=f"absent_{date_key}_{student_id}",
                    use_container_width=True,
                    type="secondary"
                ):
                    st.session_state[status_key] = "Absent"

                    st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)

        # ---------------- ATTENDANCE SUMMARY ----------------

        st.markdown("")
        st.markdown("### 📊 Attendance Summary")

        present_count = sum(
            st.session_state[f"status_{date_key}_{s['id']}"] == "Present"
            for s in students
        )

        absent_count = sum(
            st.session_state[f"status_{date_key}_{s['id']}"] == "Absent"
            for s in students
        )

        unmarked_count = len(students) - present_count - absent_count

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total Students", len(students))
        col2.metric("🟢 Present", present_count)
        col3.metric("🔴 Absent", absent_count)
        col4.metric("Not Marked", unmarked_count)

        # ---------------- SAVE ALL ATTENDANCE ----------------

        st.markdown("")

        if st.button(
            "💾 Save All Attendance",
            use_container_width=True,
            type="primary"
        ):

            if unmarked_count > 0:

                st.error(
                    f"{unmarked_count} student(s) are still not marked. "
                    "Please mark everyone before saving."
                )

            else:

                try:

                    batch = db.batch()

                    for student in students:

                        student_id = student["id"]

                        status = st.session_state[
                            f"status_{date_key}_{student_id}"
                        ]

                        record_id = f"{student_id}_{date_key}"

                        attendance_data = {
                            "student_id": student_id,
                            "student_name": student["name"],
                            "roll_number": student["roll"],
                            "date": date_key,
                            "status": status
                        }

                        attendance_ref = db.collection(
                            "attendance"
                        ).document(record_id)

                        batch.set(
                            attendance_ref,
                            attendance_data
                        )

                    batch.commit()

                    st.success(
                        f"Attendance successfully saved for "
                        f"all {len(students)} students!"
                    )

                    st.balloons()

                except Exception as e:

                    st.error(f"Unable to save attendance: {e}")

except Exception as e:

    st.error(f"Unable to load or save attendance: {e}")

# ---------------- FOOTER ----------------

st.html("""
<div style="
    text-align: center;
    padding: 20px 0 10px 0;
    color: #85819e;
    font-size: 12px;
">
    ATTENDIFY • CLOUD-BASED STUDENT ATTENDANCE MANAGEMENT
</div>
""")