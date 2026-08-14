import streamlit as st
import plotly.express as px
from pathlib import Path
import sys
import plotly.io as pio
from assets.sidebar_style import apply_sidebar_style

pio.templates.default = "plotly_white"

# Get project root directory
ROOT_DIR = Path(__file__).resolve().parents[1]
# Add root directory to Python path
sys.path.append(str(ROOT_DIR))

st.set_page_config(
    page_title="AI-Powered Customer Targeting",
    layout="wide"
)

# -------------------------
# Load custom css
# -------------------------
css_file = ROOT_DIR / "assets" / "styles.css"
with open(css_file) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
apply_sidebar_style()

# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("Recommended Audience")
st.caption("Understand the characteristics and behavioral patterns of customers identified by the AI.")
st.write("")

if "campaign" not in st.session_state:
    st.warning("No campaign has been generated yet.\n\nGo to **Decision Center** and generate a recommendation first.")
    st.stop()

campaign = st.session_state.campaign
results = campaign["results"]
outreach = campaign["outreach"]
strategy = campaign["strategy"]
df = campaign["uploaded_data"]

# --------------------------------------------------
# Overall Customer Profile
# --------------------------------------------------

st.subheader("Overall Customer Profile")
#st.caption("A summary of customers recommended for the selected campaign strategy.")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    with st.container(border=True):
            st.markdown("###### Selected Customers")
            st.markdown(
                f"<h3 style='margin:0'>{len(outreach):,}</h3>",
                unsafe_allow_html=True,)

with kpi2:
    with st.container(border=True):
            st.markdown("###### Average Likelihood")
            st.markdown(
                f"<h3 style='margin:0'>{outreach['interest_score'].mean() * 100:.1f}</h3>",
                unsafe_allow_html=True,)

with kpi3:
    with st.container(border=True):
            st.markdown("###### Average Age")
            st.markdown(
                f"<h3 style='margin:0'>{outreach['age'].mean():.1f}</h3>",
                unsafe_allow_html=True,)

with kpi4:
    with st.container(border=True):
            st.markdown("###### Average Balance")
            st.markdown(
                f"<h3 style='margin:0'>{outreach['balance'].mean():,.0f}</h3>",
                unsafe_allow_html=True,)


## --------------------------------------------------
# Customer Characteristics
# --------------------------------------------------

st.subheader("Customer Characteristics")
#st.caption("Explore the demographic profile of customers recommended for the campaign.")

left, right = st.columns(2)

with left:
    with st.container(border=True):
        st.markdown("##### Age Distribution")
        fig = px.histogram(
            outreach,
            x="age",
            nbins=20,
            labels={"age": "Age"},
        )
        
        fig.update_traces(
             marker_color="#2563EB",
            ##opacity=0.80,
            marker_line_width=0
        )
        
        fig.update_layout(
            xaxis_title="Age",
            yaxis_title="Number of Customers",
            margin=dict(l=20, r=20, t=20, b=20),
            height=320,
            bargap= 0.1 
        )
        st.plotly_chart(fig, use_container_width=True , config={"displayModeBar": False})

with right:
    with st.container(border=True):
        st.markdown("##### Occupation Distribution")
        job_counts = (
            outreach["job"]
            .value_counts()
            .reset_index()
        )
        job_counts.columns = ["Job", "Customers"]
        
        fig = px.bar(
            job_counts,
            x="Customers",
            y="Job",
            orientation="h",
        )
        
        colors = [
            "#2563EB",  # 1st
            "#3B82F6",  # 2nd
            "#60A5FA",  # 3rd
        ]
        
        # Make all remaining bars the same color as the 4th shade
        colors.extend(["#93C5FD"] * (len(job_counts) - 3))
        
        fig.update_traces(
        marker_color=colors[:len(job_counts)],
        marker_line_width=0,)

        fig.update_layout(
            yaxis=dict(categoryorder="total ascending"),
            margin=dict(l=20, r=20, t=20, b=20),
            height=320,
            showlegend=False,
            bargap=0.1
        )
        st.plotly_chart(fig, use_container_width=True , config={"displayModeBar": False})
        
st.markdown("<br>", unsafe_allow_html=True)

left, right = st.columns(2)
with left:
    with st.container(border=True):
        st.markdown("##### Education Level")
        education = (
            outreach["education"]
            .value_counts()
            .reset_index()
        )
        education.columns = ["Education", "Customers"]
        fig = px.bar(
            education,
            x="Education",
            y="Customers",
            color_discrete_sequence=["#2563EB"]
        )
         
        # Make all remaining bars the same color as the 4th shade
        colors.extend(["#93C5FD"] * (len(education.columns) - 3))
        
        fig.update_traces(
        marker_color=colors[:len(job_counts)],
        marker_line_width=0,
        width= 0.3)
        
        fig.update_layout(
            margin=dict(l=20, r=20, t=20, b=20),
            height=320,
            showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True , config={"displayModeBar": False} )
    

with right:
    with st.container(border=True):
        st.markdown("##### Marital Status")
        marital = (
            outreach["marital"]
            .value_counts()
            .reset_index()
        )
        marital.columns = ["Marital Status", "Customers"]
        fig = px.pie(
            marital,
            names="Marital Status",
            values="Customers",
            hole=0.55,
            color_discrete_sequence=[
                  "#2563EB",
        "#20C253",
        "#FFD200"
    ]
        )
        fig.update_traces(textinfo="percent+label", 
                          pull=0.01)
        fig.update_layout(
            margin=dict(l=20, r=20, t=20, b=20),
            height=320,
        )
        st.plotly_chart(fig, use_container_width=True , config={"displayModeBar": False})


# --------------------------------------------------
# Customer Behavior
# --------------------------------------------------

st.subheader("Customer Demographics")
#st.caption("Understand the likelihood and characteristics of customers selected by the AI.")

left, right = st.columns(2)

with left:
    with st.container(border=True):
        st.markdown("##### Predicted Subscription Likelihood")
        fig = px.histogram(
            outreach,
            x="interest_score",
            nbins=20,
            labels={"interest_score": "Likelihood"},
        )
        
        fig.update_traces(
             marker_color="#2563EB",
            marker_line_width=0
        )
        
        fig.update_layout(
            xaxis_tickformat=".0%",
            xaxis_title="Likelihood",
            yaxis_title="Customers",
            margin=dict(l=20, r=20, t=20, b=20),
            height=320,
            bargap= 0.1
        )
        st.plotly_chart(fig, use_container_width=True , config={"displayModeBar": False})

with right:
    with st.container(border=True):
        st.markdown("##### Customers with Housing Loans")
        housing = (
            outreach["housing"]
            .value_counts()
            .reset_index()
        )
        housing.columns = ["Housing Loan", "Customers"]
        fig = px.pie(
            housing,
            names="Housing Loan",
            values="Customers",
            hole=0.55,
            color_discrete_sequence=[
        "#2563EB",
        "#FFD200"
    ]
        )
        fig.update_traces(textinfo="percent+label", 
                          pull=0.01)
        fig.update_layout(
            margin=dict(l=20, r=20, t=20, b=20),
            height=320,
        )
        st.plotly_chart(fig, use_container_width=True , config={"displayModeBar": False})

# --------------------------------------------------
# AI Summary
# --------------------------------------------------

st.subheader("Executive Summary")

with st.container(border=True):

    # ---------- Age ----------
    overall_age = df["age"].mean()
    recommended_age = outreach["age"].mean()
    age_diff = recommended_age - overall_age

    if abs(age_diff) < 1:
        age_text = (f"Recommended customers have a similar age profile to the overall customer population.")
    elif age_diff > 0:
        age_text = (
        f"Recommended customers are on average "
        f"**{age_diff:.1f} years older** "
        f"({recommended_age:.1f} vs {overall_age:.1f} years).")
    else:
        age_text = (
        f"Recommended customers are on average "
        f"**{abs(age_diff):.1f} years younger** "
        f"({recommended_age:.1f} vs {overall_age:.1f} years).")

    # ---------- Occupation ----------
    overall_jobs = df["job"].value_counts(normalize=True)
    recommended_jobs = outreach["job"].value_counts(normalize=True)

    job_diff = (
        recommended_jobs.subtract(overall_jobs, fill_value=0)
        .sort_values(ascending=False)
    )
    
    top_job = job_diff.idxmax()
    job_change = job_diff[top_job]
    
    if job_change > 0:
        job_text = (
            f"**{top_job.title()}** customers appear more frequently in the recommended group "
            "than in the overall customer population."
        )
    else:
        job_text = (
            f"**{top_job.title()}** customers appear less frequently in the recommended group "
            "than in the overall customer population."
        )


    # ---------- Housing ----------
    overall_no_housing = (df["housing"] == "no").mean()
    recommended_no_housing = (outreach["housing"] == "no").mean()

    if recommended_no_housing > overall_no_housing:
        housing_text = (
            f"Customers without a housing loan account for "
            f"**{recommended_no_housing:.1%}** of the recommended group, "
            f"up from **{overall_no_housing:.1%}** in the overall customer population."
        )

    elif recommended_no_housing < overall_no_housing:
        housing_text = (
            f"Customers without a housing loan account for "
            f"**{recommended_no_housing:.1%}** of the recommended group, "
            f"down from **{overall_no_housing:.1%}** in the overall customer population."
        )

    else:
        housing_text = (
            f"Customers without a housing loan account for "
            f"**{recommended_no_housing:.1%}** of both the recommended group "
            "and the overall customer population."
        )

    # ---------- Education ----------
    overall_edu = df["education"].value_counts(normalize=True)
    recommended_edu = outreach["education"].value_counts(normalize=True)

    edu_diff = (
        recommended_edu.subtract(overall_edu, fill_value=0)
        .sort_values(ascending=False)
    )

    top_edu = edu_diff.index[0]
    overall_edu_pct = overall_edu.get(top_edu, 0)
    recommended_edu_pct = recommended_edu.get(top_edu, 0)

    if recommended_edu_pct > overall_edu_pct:
        education_text = (
            f"Customers with **{top_edu}** education represent "
            f"**{recommended_edu_pct:.1%}** of the recommended group, "
            f"compared with **{overall_edu_pct:.1%}** of the overall customer population."
        )
    else:
        education_text = (
            f"Customers with **{top_edu}** education represent "
            f"**{recommended_edu_pct:.1%}** of the recommended group, "
            f"compared with **{overall_edu_pct:.1%}** of the overall customer population."
        )

    st.markdown(f"""
                - {age_text}
                - {job_text}
                - {education_text}
                - {housing_text}
                """)
    
