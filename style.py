import streamlit as st


def apply_custom_style():

    st.markdown("""
    <style>

    /* =================================
       ATTENDIFY - DARK AURORA THEME
    ================================= */

    :root {
        --bg: #070A18;
        --panel: #10142B;
        --purple: #843CFF;
        --violet: #A45CFF;
        --blue: #168BFF;
        --cyan: #19C8FF;
        --green: #10C99A;
        --white: #F7F5FF;
        --muted: #B9B9D8;
    }

    /* MAIN BACKGROUND */

    .stApp {
        background:
            radial-gradient(ellipse at 5% 10%,
                rgba(105, 39, 210, 0.25), transparent 32%),
            radial-gradient(ellipse at 95% 90%,
                rgba(0, 130, 255, 0.20), transparent 35%),
            radial-gradient(ellipse at 55% 45%,
                rgba(50, 30, 110, 0.10), transparent 50%),
            #070A18;

        color: var(--white);
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2.5rem;
        max-width: 1500px;
    }

    /* SIDEBAR */

    section[data-testid="stSidebar"] {
        background:
            radial-gradient(circle at 10% 10%,
                rgba(126, 48, 255, 0.25), transparent 35%),
            linear-gradient(180deg, #100D25, #0A1022);

        border-right: 1px solid rgba(140, 100, 255, 0.35);
    }

    section[data-testid="stSidebar"] * {
        color: #EAE7FF;
    }

    section[data-testid="stSidebar"] a {
        border-radius: 10px;
        transition: all 0.25s ease;
    }

    section[data-testid="stSidebar"] a:hover {
        background: rgba(126, 70, 255, 0.22);
        box-shadow: 0 0 18px rgba(126, 70, 255, 0.18);
    }

    /* HEADINGS */

    h1, h2, h3 {
        color: #F8F6FF !important;
        font-weight: 750 !important;
    }

    p, label {
        color: #C8C8E3;
    }

    /* GLASS PANELS */

    div[data-testid="stMetric"] {
        background:
            radial-gradient(circle at 100% 100%,
                rgba(126, 61, 255, 0.22), transparent 45%),
            linear-gradient(135deg,
                rgba(39, 31, 83, 0.92),
                rgba(14, 23, 53, 0.95));

        border: 1px solid rgba(153, 112, 255, 0.40);
        border-radius: 17px;
        padding: 22px;

        box-shadow:
            0 8px 30px rgba(0, 0, 0, 0.30),
            inset 0 1px 0 rgba(255,255,255,0.06);

        position: relative;
        overflow: hidden;
    }

    div[data-testid="stMetricLabel"] {
        color: #D0C9F2 !important;
    }

    div[data-testid="stMetricValue"] {
        color: #FFFFFF !important;
        font-size: 32px !important;
        font-weight: 800 !important;
    }

    /* BUTTONS */

    .stButton > button,
    .stFormSubmitButton > button {
        background: linear-gradient(110deg, #7935E9, #236EEB);
        color: white !important;
        border: 1px solid rgba(190, 160, 255, 0.35);
        border-radius: 10px;
        font-weight: 700;
        transition: 0.25s ease;
    }

    .stButton > button:hover,
    .stFormSubmitButton > button:hover {
        box-shadow: 0 0 22px rgba(132, 60, 255, 0.65);
        transform: translateY(-2px);
    }

    /* INPUT FIELDS */

    .stTextInput input,
    .stNumberInput input,
    .stDateInput input,
    .stTextArea textarea {
        background: #151A35 !important;
        color: white !important;
        border: 1px solid #51447F !important;
        border-radius: 9px !important;
    }

    .stSelectbox div[data-baseweb="select"] {
        background: #151A35 !important;
        border-radius: 9px !important;
    }

    /* FORMS */

    div[data-testid="stForm"] {
        background: rgba(20, 23, 52, 0.78);
        border: 1px solid rgba(145, 112, 255, 0.30);
        border-radius: 16px;
        padding: 24px;
    }

    /* DATA TABLES */

    div[data-testid="stDataFrame"] {
        border: 1px solid rgba(130, 100, 230, 0.35);
        border-radius: 12px;
        overflow: hidden;
    }

    /* DIVIDERS */

    hr {
        border-color: rgba(140, 110, 255, 0.22);
    }

    /* CHART TEXT */

    .stPlotlyChart {
        background: transparent;
        border-radius: 14px;
    }

    /* RADIO BUTTONS */

    div[role="radiogroup"] label {
        color: #E8E4FF !important;
    }

    /* SUCCESS MESSAGES */

    div[data-testid="stAlert"] {
        border-radius: 12px;
    }

    /* SCROLLBAR */

    ::-webkit-scrollbar {
        width: 8px;
    }

    ::-webkit-scrollbar-track {
        background: #090C1B;
    }

    ::-webkit-scrollbar-thumb {
        background: linear-gradient(#873DFF, #168BFF);
        border-radius: 10px;
    }

    </style>
    """, unsafe_allow_html=True)


def render_aurora_banner():

    st.markdown("""
    <div class="aurora-banner">

        <div class="aurora-decoration"></div>

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
        position: relative;
        overflow: hidden;
        min-height: 190px;
        padding: 35px 38px;

        border-radius: 18px;
        border: 1px solid rgba(142, 84, 255, 0.45);

        background:
            radial-gradient(ellipse at 90% 100%,
                rgba(106, 35, 255, 0.65), transparent 38%),
            radial-gradient(ellipse at 70% 90%,
                rgba(0, 145, 255, 0.42), transparent 38%),
            linear-gradient(110deg,
                #211044 0%,
                #101438 55%,
                #111D54 100%);

        box-shadow:
            0 10px 40px rgba(30, 10, 90, 0.28),
            inset 0 1px 0 rgba(255,255,255,0.08);
    }

    .aurora-banner::before {
        content: "";
        position: absolute;
        width: 65%;
        height: 150px;
        right: -5%;
        bottom: -90px;

        border-radius: 50%;
        border-top: 3px solid #27B7FF;

        transform: rotate(-12deg);

        box-shadow:
            0 -12px 25px rgba(20, 150, 255, 0.35),
            0 -25px 45px rgba(125, 50, 255, 0.28);
    }

    .aurora-banner::after {
        content: "";
        position: absolute;
        width: 55%;
        height: 130px;
        right: -8%;
        bottom: -90px;

        border-radius: 50%;
        border-top: 3px solid #A94DFF;

        transform: rotate(-18deg);

        box-shadow: 0 -10px 35px rgba(150, 50, 255, 0.50);
    }

    .banner-content {
        position: relative;
        z-index: 2;
    }

    .banner-title {
        color: #FFFFFF;
        font-size: clamp(27px, 3vw, 43px);
        font-weight: 800;
        letter-spacing: -1px;
    }

    .banner-title span {
        background: linear-gradient(90deg, #B66AFF, #508CFF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .banner-subtitle {
        font-size: 19px;
        color: #E6E4FF;
        margin-top: 7px;
    }

    .banner-tagline {
        margin-top: 20px;
        padding-left: 14px;
        border-left: 4px solid #A34CFF;
        color: #D6CBFF;
        font-size: 15px;
    }

    .graduation-cap {
        position: absolute;
        z-index: 1;
        right: 7%;
        top: 25%;
        font-size: 75px;
        filter: drop-shadow(0 0 18px #704DFF);
        opacity: 0.9;
    }

    </style>
    """, unsafe_allow_html=True)


def render_section_title(title, subtitle=""):

    st.html(f"""
    <div style="
        margin: 24px 0 14px 0;
    ">
        <div style="
            font-size: 23px;
            font-weight: 750;
            color: #F6F3FF;
        ">{title}</div>

        <div style="
            font-size: 13px;
            color: #AAA8CC;
            margin-top: 5px;
        ">{subtitle}</div>
    </div>
    """)