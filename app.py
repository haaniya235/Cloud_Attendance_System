import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from html import escape

from firebase_config import db
from style import apply_custom_style
from auth import require_auth


st.set_page_config(
    page_title="Attendify | Admin Dashboard",
    page_icon="🎓",
    layout="wide"
)
if not require_auth():
    st.stop()
# Apply Dark Aurora theme
apply_custom_style()


# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.html("""
    <div style="padding:15px 5px 30px 5px;">
        <div style="font-size:30px;">
            🎓 <b>Attendify</b>
        </div>
        <div style="font-size:11px;color:#AAA8CC;margin-left:43px;">
            Track • Manage • Excel
        </div>
    </div>
    """)

    st.html("""
    <div style="
        margin-top:40px;
        padding:12px;
        border-radius:10px;
        background:linear-gradient(100deg,#7138D8,#30205C);
        color:white;
        font-weight:700;">
        🏠 &nbsp; Home
    </div>
    """)

    st.html("""
    <div style="padding:14px 10px;color:#D8D4F5;">
        👥 &nbsp; Student Registration<br><br>
        ☑️ &nbsp; Mark Attendance<br><br>
        ◉ &nbsp; View Attendance<br><br>
        ▥ &nbsp; Attendance Reports
    </div>
    """)

    st.html("""
    <div style="
        margin-top:100px;
        padding:15px 5px;
        color:#AAA8CC;
        font-size:12px;
        text-align:center;">
        🎓<br>Attendify v1.0<br><br>© 2026
    </div>
    """)


# ==================================================
# WELCOME BANNER
# ==================================================

st.html("""
<div class="aurora-banner">

    <div class="banner-content">

        <div class="banner-title">
            Welcome to <span>Attendify</span>
        </div>

        <div class="banner-subtitle">
            Cloud-Based Student Attendance Management System
        </div>

        <div class="banner-tagline">
            Smart. Secure. Seamless.
        </div>

    </div>

    <div class="graduation-cap">🎓</div>

</div>

<style>

.aurora-banner {
    position:relative;
    overflow:hidden;
    min-height:190px;
    padding:35px 38px;
    border-radius:18px;
    border:1px solid rgba(142,84,255,0.45);
    background:
        radial-gradient(ellipse at 90% 100%,
        rgba(106,35,255,0.65),transparent 38%),
        radial-gradient(ellipse at 70% 90%,
        rgba(0,145,255,0.42),transparent 38%),
        linear-gradient(110deg,#211044 0%,#101438 55%,#111D54 100%);
    box-shadow:0 10px 40px rgba(30,10,90,0.28);
}

.aurora-banner::before {
    content:"";
    position:absolute;
    width:65%;
    height:150px;
    right:-5%;
    bottom:-90px;
    border-radius:50%;
    border-top:3px solid #27B7FF;
    transform:rotate(-12deg);
    box-shadow:
        0 -12px 25px rgba(20,150,255,0.35),
        0 -25px 45px rgba(125,50,255,0.28);
}

.aurora-banner::after {
    content:"";
    position:absolute;
    width:55%;
    height:130px;
    right:-8%;
    bottom:-90px;
    border-radius:50%;
    border-top:3px solid #A94DFF;
    transform:rotate(-18deg);
    box-shadow:0 -10px 35px rgba(150,50,255,0.50);
}

.banner-content {
    position:relative;
    z-index:2;
}

.banner-title {
    color:#FFFFFF;
    font-size:clamp(27px,3vw,43px);
    font-weight:800;
    letter-spacing:-1px;
}

.banner-title span {
    background:linear-gradient(90deg,#B66AFF,#508CFF);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}

.banner-subtitle {
    font-size:19px;
    color:#E6E4FF;
    margin-top:7px;
}

.banner-tagline {
    margin-top:20px;
    padding-left:14px;
    border-left:4px solid #A34CFF;
    color:#D6CBFF;
    font-size:15px;
}

.graduation-cap {
    position:absolute;
    z-index:2;
    right:7%;
    top:25%;
    font-size:75px;
    filter:drop-shadow(0 0 18px #704DFF);
}

</style>
""")


# ==================================================
# FETCH LIVE FIREBASE DATA
# ==================================================

try:

    student_docs = list(db.collection("students").stream())
    attendance_docs = list(db.collection("attendance").stream())

    student_count = len(student_docs)

    records = []

    for doc in attendance_docs:

        data = doc.to_dict()

        records.append({
            "Date": data.get("date", ""),
            "Student Name": data.get("student_name", ""),
            "Roll Number": data.get("roll_number", ""),
            "Status": data.get("status", "")
        })

    df = pd.DataFrame(records)

    total_records = len(df)

    if total_records > 0:

        present = int((df["Status"] == "Present").sum())
        absent = int((df["Status"] == "Absent").sum())

        attendance_rate = (present / total_records) * 100

    else:

        present = 0
        absent = 0
        attendance_rate = 0


    # ==================================================
    # DASHBOARD OVERVIEW
    # ==================================================

    st.html("""
    <div style="margin:24px 0 14px 0;">

        <div style="
            font-size:23px;
            font-weight:750;
            color:#F6F3FF;">
            Dashboard Overview
        </div>

        <div style="
            font-size:13px;
            color:#AAA8CC;
            margin-top:5px;">
            Your attendance statistics at a glance
        </div>

    </div>
    """)


    # ==================================================
    # STATISTICS CARDS
    # ==================================================

    def stat_card(icon, label, value, theme):

        themes = {
            "purple": ("#7135E8", "#28134D", "#9D65FF"),
            "blue": ("#1678DF", "#10264C", "#36A9FF"),
            "green": ("#079C7B", "#103D3C", "#25DDB1"),
            "violet": ("#7536D9", "#281448", "#A36AFF")
        }

        start, end, glow = themes[theme]

        st.html(f"""
        <div style="
            min-height:112px;
            padding:19px;
            border-radius:17px;
            position:relative;
            overflow:hidden;
            border:1px solid {glow}66;
            background:
                radial-gradient(circle at 100% 100%,
                {glow}55,transparent 42%),
                linear-gradient(125deg,{end},{start}33);
            box-shadow:0 8px 25px #00000040;
            display:flex;
            align-items:center;
            gap:15px;">

            <div style="
                width:58px;
                height:58px;
                min-width:58px;
                border-radius:50%;
                background:{start};
                display:flex;
                align-items:center;
                justify-content:center;
                font-size:27px;
                box-shadow:0 0 20px {glow}77;">
                {icon}
            </div>

            <div>
                <div style="font-size:14px;color:#DAD8F5;">
                    {escape(label)}
                </div>

                <div style="
                    font-size:29px;
                    font-weight:800;
                    color:white;">
                    {escape(str(value))}
                </div>
            </div>

        </div>
        """)


    c1, c2, c3, c4 = st.columns(4)

    with c1:
        stat_card("👥", "Registered Students", student_count, "purple")

    with c2:
        stat_card("▦", "Attendance Records", total_records, "blue")

    with c3:
        stat_card("✓", "Present", present, "green")

    with c4:
        stat_card(
            "▥",
            "Attendance Rate",
            f"{attendance_rate:.1f}%",
            "violet"
        )


    # ==================================================
    # CHART AND RECENT ATTENDANCE
    # ==================================================

    st.html("<div style='height:25px;'></div>")

    chart_col, table_col = st.columns([1.08, 1])


    # ==================================================
    # ATTENDANCE OVERVIEW CHART
    # ==================================================

    with chart_col:

        st.html("""
        <div style="
            font-size:21px;
            font-weight:750;
            color:#F6F3FF;
            padding:10px 0;">
            ▥ &nbsp; Attendance Overview
        </div>
        """)

        fig = go.Figure()

        fig.add_trace(go.Bar(

            x=["Present", "Absent"],

            y=[present, absent],

            marker=dict(
                color=["#963DFF", "#268CFF"],
                line=dict(
                    color=["#C18AFF", "#65BDFF"],
                    width=2
                )
            ),

            text=[str(present), str(absent)],

            textposition="outside",

            textfont=dict(
                color="#FFFFFF",
                size=16,
                family="Arial"
            ),

            width=0.42,

            hovertemplate="%{x}: %{y}<extra></extra>"
        ))

        fig.update_layout(

            height=330,

            paper_bgcolor="rgba(0,0,0,0)",

            plot_bgcolor="rgba(0,0,0,0)",

            font=dict(
                color="#E8E4FF",
                family="Arial"
            ),

            margin=dict(l=35, r=25, t=35, b=40),

            showlegend=False,

            bargap=0.55,

            yaxis=dict(
                rangemode="tozero",
                gridcolor="rgba(151,110,255,0.16)",
                zerolinecolor="rgba(151,110,255,0.25)",
                title=None
            ),

            xaxis=dict(
                title=None,
                showgrid=False,
                tickfont=dict(
                    color="#E8E4FF",
                    size=14
                )
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False}
        )


    # ==================================================
    # RECENT ATTENDANCE RECORDS
    # ==================================================

    with table_col:

        st.html("""
        <div style="
            display:flex;
            justify-content:space-between;
            align-items:center;
            padding:10px 0;
            font-size:21px;
            font-weight:750;
            color:#F6F3FF;">
            ▤ &nbsp; Recent Attendance Records
        </div>
        """)

        if not df.empty:

            recent = df.copy()

            recent["_sort_date"] = pd.to_datetime(
                recent["Date"],
                errors="coerce"
            )

            recent = recent.sort_values(
                "_sort_date",
                ascending=False
            ).head(8)

            rows_html = ""

            for _, row in recent.iterrows():

                status = str(row["Status"])

                if status == "Present":

                    badge = """
                    <span style="
                        background:#087D65;
                        color:white;
                        padding:6px 11px;
                        border-radius:20px;">
                        ✓ Present
                    </span>
                    """

                else:

                    badge = """
                    <span style="
                        background:#9B354D;
                        color:white;
                        padding:6px 11px;
                        border-radius:20px;">
                        Absent
                    </span>
                    """

                rows_html += f"""
                <tr>
                    <td>{escape(str(row["Date"]))}</td>
                    <td>{escape(str(row["Student Name"]))}</td>
                    <td>{escape(str(row["Roll Number"]))}</td>
                    <td>{badge}</td>
                </tr>
                """

            st.html(f"""
            <div style="
                border:1px solid #45366F;
                border-radius:13px;
                overflow-x:auto;
                background:#10142B;">

                <table style="
                    width:100%;
                    border-collapse:collapse;
                    color:#F3F0FF;
                    font-size:13px;">

                    <thead style="background:#292052;">

                        <tr>
                            <th style="padding:14px;text-align:left;">Date</th>
                            <th style="padding:14px;text-align:left;">Student Name</th>
                            <th style="padding:14px;text-align:left;">Roll Number</th>
                            <th style="padding:14px;text-align:left;">Status</th>
                        </tr>

                    </thead>

                    <tbody>
                        {rows_html}
                    </tbody>

                </table>

            </div>

            <style>
                td {{
                    padding:14px;
                    border-top:1px solid #292747;
                    white-space:nowrap;
                }}
            </style>
            """)

        else:

            st.info("No attendance records available yet.")


    # ==================================================
    # FOOTER
    # ==================================================

    st.html("""
    <div style="
        margin-top:45px;
        text-align:center;
        color:#AAA8CC;
        font-size:12px;">
        ━━━━━━━━━━━ &nbsp; Attendify &nbsp; | &nbsp;
        Cloud-Based Student Attendance Management System
        &nbsp; ━━━━━━━━━━━
    </div>
    """)


except Exception as e:

    st.error(f"Unable to load dashboard data: {e}")