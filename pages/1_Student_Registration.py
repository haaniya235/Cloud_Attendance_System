import streamlit as st
from firebase_config import db
from style import apply_custom_style
from auth import require_auth

# ---------------- PAGE CONFIGURATION ----------------

st.set_page_config(
    page_title="Student Registration",
    page_icon="🎓",
    layout="wide"
)

if not require_auth():
    st.stop()
apply_custom_style()

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
    ">ATTENDIFY • STUDENT MANAGEMENT</div>

    <div style="
        color: white;
        font-size: 30px;
        font-weight: 750;
        margin-bottom: 8px;
    ">🎓 Student Registration</div>

    <div style="
        color: #c2bfd8;
        font-size: 15px;
    ">
        Add new students to your cloud-based attendance system.
        Their details will be securely saved in Firebase.
    </div>
</div>
""")

# ---------------- SECTION HEADING ----------------

st.markdown("### ✨ Student Information")
st.caption("Enter the student's details below. Fields marked with * are required.")

st.markdown("")

# ---------------- REGISTRATION FORM ----------------

with st.form("student_registration_form", clear_on_submit=False):

    st.markdown("#### Personal Details")

    col1, col2 = st.columns(2)

    with col1:
        student_id = st.text_input(
            "Student ID *",
            placeholder="Example: STU004"
        )

        student_name = st.text_input(
            "Student Name *",
            placeholder="Enter full name"
        )

        roll_number = st.text_input(
            "Roll Number *",
            placeholder="Enter roll number"
        )

    with col2:
        student_class = st.text_input(
            "Class *",
            placeholder="Example: MSc Data Science"
        )

        email = st.text_input(
            "Email Address",
            placeholder="student@example.com"
        )

        phone = st.text_input(
            "Phone Number",
            placeholder="Enter phone number"
        )

    st.markdown("")
    st.caption("* Required fields")

    submit = st.form_submit_button(
        "✦  Register Student",
        use_container_width=True
    )

    # ---------------- FORM VALIDATION ----------------

    if submit:

        if not all([
            student_id.strip(),
            student_name.strip(),
            roll_number.strip(),
            student_class.strip()
        ]):
            st.error(
                "Please fill in Student ID, Name, Roll Number and Class."
            )

        else:
            try:
                student_ref = db.collection("students").document(
                    student_id.strip()
                )

                if student_ref.get().exists:

                    st.error(
                        "This Student ID is already registered. "
                        "Please use a different ID."
                    )

                else:
                    student_data = {
                        "student_id": student_id.strip(),
                        "student_name": student_name.strip(),
                        "roll_number": roll_number.strip(),
                        "class": student_class.strip(),
                        "email": email.strip(),
                        "phone": phone.strip()
                    }

                    student_ref.set(student_data)

                    st.success(
                        f"Student {student_name.strip()} registered successfully!"
                    )

                    st.balloons()

            except Exception as e:
                st.error(f"Error registering student: {e}")

# ---------------- FOOTER ----------------

st.markdown("")

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