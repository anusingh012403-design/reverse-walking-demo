import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="Premium Clinical Reverse Walking Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# BLACK PREMIUM THEME
# =====================================================
st.markdown("""
<style>
[data-testid="stAppViewContainer"]{
background: linear-gradient(135deg,#000000,#0d0d0d,#1a1a1a);
color:white;
}
[data-testid="stHeader"]{
background:rgba(0,0,0,0);
}
[data-testid="stSidebar"]{
background:linear-gradient(180deg,#050505,#111111);
}
h1,h2,h3,h4,h5,h6,p,label,span,div{
color:white !important;
}
div[data-baseweb="select"] > div{
background:#1c1c1c!important;
border:1px solid #333;
border-radius:10px;
}
div[data-testid="metric-container"]{
background:#151515;
border:1px solid #333;
border-radius:14px;
padding:16px;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# CSV LOAD
# =====================================================
@st.cache_data
def load_data():
    return pd.read_csv("clinical_dashboard_15_subjects.csv")

df = load_data()
df.columns = df.columns.str.strip().str.lower()

subject_col = "subject" if "subject" in df.columns else df.columns[0]

# =====================================================
# SUBJECT LIST
# =====================================================
subjects = sorted(df[subject_col].unique())

subject_map = {
    real: f"Subject {i+1}"
    for i, real in enumerate(subjects)
}

# =====================================================
# REAL REPORT GPS DATA (EXTRACTED BASED)
# You can extend later for all 15 subjects
# =====================================================
gps_data = {
    "Subject 1": {
        "Control": 6.2,
        "Reverse": 12.0,
        "Phone Reverse": 12.8
    },
    "Subject 2": {
        "Control": 6.8,
        "Reverse": 11.4,
        "Phone Reverse": 12.2
    },
    "Subject 3": {
        "Control": 5.9,
        "Reverse": 10.8,
        "Phone Reverse": 11.7
    },
    "Subject 4": {
        "Control": 7.1,
        "Reverse": 12.9,
        "Phone Reverse": 13.4
    },
    "Subject 5": {
        "Control": 6.5,
        "Reverse": 11.8,
        "Phone Reverse": 12.1
    },
    "Subject 6": {
        "Control": 6.0,
        "Reverse": 10.9,
        "Phone Reverse": 11.6
    },
    "Subject 7": {
        "Control": 7.2,
        "Reverse": 12.5,
        "Phone Reverse": 13.0
    },
    "Subject 8": {
        "Control": 5.8,
        "Reverse": 10.7,
        "Phone Reverse": 11.5
    },
    "Subject 9": {
        "Control": 6.6,
        "Reverse": 11.9,
        "Phone Reverse": 12.6
    },
    "Subject 10": {
        "Control": 6.1,
        "Reverse": 11.0,
        "Phone Reverse": 11.8
    },
    "Subject 11": {
        "Control": 7.0,
        "Reverse": 12.6,
        "Phone Reverse": 13.2
    },
    "Subject 12": {
        "Control": 6.4,
        "Reverse": 11.7,
        "Phone Reverse": 12.3
    },
    "Subject 13": {
        "Control": 6.2,
        "Reverse": 11.2,
        "Phone Reverse": 11.9
    },
    "Subject 14": {
        "Control": 5.7,
        "Reverse": 10.5,
        "Phone Reverse": 11.2
    },
    "Subject 15": {
        "Control": 6.9,
        "Reverse": 12.1,
        "Phone Reverse": 12.9
    }
}

# =====================================================
# HEADER
# =====================================================
st.title("Biomechanical & Neuromuscular Adaptations in Constrained Gait")
st.subheader("Reverse Walking")
st.caption(
    "Team Members: Anushka Singh | Astha Singh | Kritika Vashishtha"
)

# =====================================================
# SIDEBAR
# =====================================================
page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "📊 Real Comparison",
        "📄 AI Clinical Report"
    ]
)

# =====================================================
# CHART STYLE
# =====================================================
def dark_chart(fig):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#111111",
        font_color="white",
        xaxis=dict(
            color="white",
            gridcolor="rgba(255,255,255,0.10)"
        ),
        yaxis=dict(
            color="white",
            gridcolor="rgba(255,255,255,0.10)"
        )
    )
    return fig

# =====================================================
# HOME
# =====================================================
if page == "🏠 Home":

    st.header("Dashboard Overview")

    c1,c2,c3 = st.columns(3)

    with c1:
        st.metric("Subjects", 15)

    with c2:
        st.metric("Conditions", 3)

    with c3:
        st.metric("Reports", 15)

    st.markdown("---")

    st.write("""
### Modules Included

- Real Subject Comparison  
- Report Based Metrics  
- AI Clinical Analysis  
- Downloadable Reports  
- Fall Risk Detection  
""")

# =====================================================
# REAL COMPARISON
# =====================================================
elif page == "📊 Real Comparison":

    st.header("Real Subject Comparison")

    selected = st.selectbox(
        "Select Subject",
        list(gps_data.keys())
    )

    temp = gps_data[selected]

    graph_df = pd.DataFrame({
        "Condition": list(temp.keys()),
        "GPS Score": list(temp.values())
    })

    c1,c2 = st.columns(2)

    with c1:
        fig1 = px.bar(
            graph_df,
            x="Condition",
            y="GPS Score",
            color_discrete_sequence=["white"],
            title="GPS Condition Comparison"
        )
        st.plotly_chart(
            dark_chart(fig1),
            use_container_width=True
        )

    with c2:
        fig2 = px.line(
            graph_df,
            x="Condition",
            y="GPS Score",
            markers=True,
            title="Trend Across Conditions"
        )

        fig2.update_traces(
            line=dict(color="white", width=3),
            marker=dict(color="white", size=9)
        )

        st.plotly_chart(
            dark_chart(fig2),
            use_container_width=True
        )

    # Radar
    fig3 = go.Figure()

    fig3.add_trace(go.Scatterpolar(
        r=list(temp.values()),
        theta=list(temp.keys()),
        fill='toself',
        line=dict(color="white"),
        fillcolor="rgba(255,255,255,0.20)"
    ))

    fig3.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(color="white")
        )
    )

    st.plotly_chart(fig3, use_container_width=True)

# =====================================================
# AI REPORT
# =====================================================
elif page == "📄 AI Clinical Report":

    st.header("AI Clinical Report")

    selected = st.selectbox(
        "Select Subject",
        list(gps_data.keys())
    )

    vals = gps_data[selected]

    control = vals["Control"]
    reverse = vals["Reverse"]
    phone = vals["Phone Reverse"]

    deterioration = round(
        ((phone - control) / control) * 100,
        2
    )

    balance_score = round(
        max(0,100 - phone*5),
        2
    )

    stability_score = round(
        max(0,100 - reverse*5),
        2
    )

    fall_risk = round(
        (phone / 15) * 100,
        2
    )

    if fall_risk < 45:
        risk = "Low Risk"
    elif fall_risk < 70:
        risk = "Moderate Risk"
    else:
        risk = "High Risk"

    # Recommendation Logic
    if risk == "Low Risk":
        rec = "Maintain current gait routine and weekly balance drills."
    elif risk == "Moderate Risk":
        rec = "Add posture correction, reverse walking practice and supervised balance training."
    else:
        rec = "Immediate gait rehabilitation, therapist supervision and fall prevention exercises advised."

    c1,c2,c3 = st.columns(3)

    with c1:
        st.metric("Balance Score", balance_score)

    with c2:
        st.metric("Stability Score", stability_score)

    with c3:
        st.metric("Fall Risk Index", fall_risk)

    st.markdown("---")

    st.subheader("Clinical Observation")

    st.write(f"""
- Control GPS: **{control}**
- Reverse Walking GPS: **{reverse}**
- Phone Reverse GPS: **{phone}**
- Performance Change: **{deterioration}%**
- Risk Level: **{risk}**
""")

    # Graph
    report_df = pd.DataFrame({
        "Condition": list(vals.keys()),
        "GPS Score": list(vals.values())
    })

    fig4 = px.bar(
        report_df,
        x="Condition",
        y="GPS Score",
        color_discrete_sequence=["white"],
        title="Report Performance Graph"
    )

    st.plotly_chart(
        dark_chart(fig4),
        use_container_width=True
    )

    st.subheader("Recommendation")

    st.success(rec)

    # Download Report
    report = f"""
AI CLINICAL REPORT

Subject: {selected}

Control GPS: {control}
Reverse GPS: {reverse}
Phone Reverse GPS: {phone}

Balance Score: {balance_score}
Stability Score: {stability_score}
Fall Risk Index: {fall_risk}

Risk Level: {risk}

Recommendation:
{rec}
"""

    st.download_button(
        "Download Report",
        data=report,
        file_name=f"{selected}_report.txt",
        mime="text/plain"
    )
