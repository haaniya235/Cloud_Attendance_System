Attendify – Cloud-Based Student Attendance Management System

📌 Project Overview

Attendify is a cloud-based student attendance management system developed using Python, Streamlit, and Firebase. It provides a centralised platform for administrators to register students, record daily attendance, view attendance records, and generate reports.

The system aims to make attendance management more organised, efficient, and convenient through a simple web-based interface.

🎯 Objectives

* To simplify student registration and attendance management.
* To maintain student information in a cloud database.
* To record and retrieve daily attendance.
* To calculate individual student attendance percentages.
* To generate attendance reports and visualisations.
* To provide secure administrator authentication.

✨ Key Features

1. Admin Login

Secure administrator login using Firebase Authentication.

2. Student Registration

Register and manage student details.

3. Mark Attendance

Mark students as Present or Absent and save attendance records.

4. View Attendance

Search, filter, and view previously recorded attendance.

5. Attendance Reports

Generate attendance summaries, percentages, and interactive charts.

6. Student Profile

View individual student details, attendance statistics, and date-wise attendance history.

7. Data Export

Download attendance records in CSV and Excel formats.

🛠️ Technologies Used

Technology	Purpose
Python	Backend programming
Streamlit	Web application interface
Firebase Authentication	Administrator authentication
Firebase Admin SDK	Server-side authentication verification
Cloud Firestore	Cloud database
Pandas	Data processing
Plotly	Data visualisation
OpenPyXL	Excel report generation

📂 Project Structure

Cloud_Attendance_System/
│
├── .streamlit/
│   └── secrets.toml
│
├── pages/
│   ├── 1_Student_Registration.py
│   ├── 2_Mark_Attendance.py
│   ├── 3_View_Attendance.py
│   ├── 4_Attendance_Reports.py
│   └── 5_Student_Profile.py
│
├── app.py
├── auth.py
├── firebase_config.py
├── style.py
├── requirements.txt
├── .gitignore
└── firebase_key.json

Note: Firebase credentials and secrets are required locally but are excluded from the public GitHub repository.

⚙️ Installation and Setup

Step 1: Clone the Repository

git clone https://github.com/YOUR-USERNAME/Attendify-Cloud-Attendance-System.git

Step 2: Open the Project Folder

cd Attendify-Cloud-Attendance-System

Step 3: Create a Virtual Environment

python -m venv venv

Activate it on Windows:

venv\Scripts\activate

Step 4: Install Dependencies

pip install -r requirements.txt

Step 5: Configure Firebase

* Create a Firebase project.
* Enable Firebase Authentication with Email/Password.
* Create a Cloud Firestore database.
* Generate a Firebase Admin SDK service account key.
* Place the service account JSON file locally as firebase_key.json.
* Configure the required Firebase web settings and authorised administrator UID in .streamlit/secrets.toml.

Important: Never upload Firebase credentials, private keys, administrator identifiers, or secrets to GitHub.

Step 6: Run the Application

streamlit run app.py

The application will open in your default web browser.

🔄 System Workflow

1. The administrator logs into the application.
2. Student details are registered.
3. Attendance is manually marked as Present or Absent.
4. Attendance information is stored in Cloud Firestore.
5. The administrator can view records, generate reports, and access student profiles.

🔐 Security

* Firebase Authentication is used for administrator login.
* Server-side identity token verification is implemented.
* Administrator access is restricted using an authorised UID check.
* Firebase credentials and secrets are excluded using .gitignore.

🚀 Future Enhancements

* Student login and individual attendance access.
* Automated attendance notifications.
* Attendance prediction and analytical insights.
* Mobile-friendly interface improvements.
* Integration with additional academic management features.

⚠️ Project Scope

Attendify is an administrator-operated attendance management prototype. Attendance is entered manually by the administrator. The current implementation does not include biometric attendance, facial recognition, or automatic attendance detection.

👩‍💻 Project Information

Project Title: Cloud-Based Student Attendance Management System

Application Name: Attendify

Domain: Cloud Computing / Data Science

Developed Using: Python, Streamlit and Firebase

⸻

Attendify – Making Student Attendance Management Simple, Organised and Accessible.
