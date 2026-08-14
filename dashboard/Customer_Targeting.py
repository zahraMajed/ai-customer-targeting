import sys
from pathlib import Path
import joblib
import csv
import streamlit as st
import pandas as pd

from production.prediction import predict_customers
from production.business_metrics import calculate_dashboard_metrics
from production.reach_analysis import calculate_reach
from assets.sidebar_style import apply_sidebar_style

# Get project root directory
ROOT_DIR = Path(__file__).resolve().parents[1]
# Add root directory to Python path
sys.path.append(str(ROOT_DIR))
CONFIG_PATH = ROOT_DIR / "models" / "strategy_config.pkl"
strategy_config = joblib.load(CONFIG_PATH)

st.set_page_config(
    page_title="AI-Powered Customer Targeting",
    layout="wide",
    initial_sidebar_state="collapsed"

)

import plotly.io as pio
pio.templates.default = "plotly_white"

# -------------------------
# Load custom css & style
# -------------------------
css_file = ROOT_DIR / "dashboard" / "assets" / "styles.css"
with open(css_file) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
apply_sidebar_style()

# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("Customer Targeting")
st.caption("Upload a customer list and let the AI prioritize customers for your marketing campaign.")

# -------------------------
# Session State
# -------------------------

if "strategy" not in st.session_state:
    st.session_state.strategy = "Aggressive"

if "campaign" not in st.session_state:
    st.session_state.campaign = None
    
# -------------------------
# Campaign Planning
# -------------------------

st.subheader("Targeting Setup")
st.write("")

col1, spacer1, divider, spacer2, col2 = st.columns([1, 0.05, 0.03, 0.05, 1])

with col1:
        st.markdown("##### Upload Customer Dataset")
        uploaded_file = st.file_uploader("", type=["csv"], label_visibility="collapsed")
    
        if uploaded_file is not None:
            st.markdown(f"<span style='color:#16a34a;'>✓ {uploaded_file.name} uploaded</span>",
                        unsafe_allow_html=True)  
            current_file = uploaded_file.name
            previous_campaign = st.session_state.campaign
            if (previous_campaign is None
                or current_file != previous_campaign["file_name"]):
                st.session_state.campaign = None
        elif st.session_state.campaign is not None:
            st.markdown(f"<span style='color:#16a34a;'>Uploaded Dataset: {st.session_state.campaign['file_name']}</span>",
                        unsafe_allow_html=True) 
                
with divider:
    st.markdown(
        """
        <div style="
            border-left:1px solid #E5E7EB;
            height:260px;
            margin:auto;">
        </div>
        """,
        unsafe_allow_html=True,
    )
    
with col2:
        st.markdown("##### Campaign Objective")
            
        # Radio options (display labels)
        objective_labels = [
            config["label"]
            for config in strategy_config.values()]
        
        previous_strategy = st.session_state.strategy
        
        # Display radio buttons
        selected_label = st.radio(
            "",
            objective_labels,
            index=list(strategy_config.keys()).index(previous_strategy),
            label_visibility="collapsed")
        
        # Convert the selected label back to the strategy key
        strategy = next(key for key, value in strategy_config.items()
        if value["label"] == selected_label)
        
        # Reset analysis if strategy changes
        if strategy != previous_strategy:
            st.session_state.campaign = None
        
        # Save the selected strategy
        st.session_state.strategy = strategy

        with st.popover("💡 Objective Comparison"):
            
            for config in strategy_config.values():
                st.markdown(f"**{config['label']}**")
                st.write(config["description"])
                st.write("")   # blank line
                
        run_analysis = st.button("Generate Target Audience", type="primary")

      
strategy = st.session_state.strategy


# -----------------------------------
# Create a new campaign
# -----------------------------------
if uploaded_file is not None and run_analysis:
    
    # detect the delimiter automatically to read the file 
    sample = uploaded_file.read(1024).decode("utf-8")
    uploaded_file.seek(0)
    dialect = csv.Sniffer().sniff(sample)
    df = pd.read_csv(uploaded_file, sep=dialect.delimiter)
    
    # Make predictions
    results = predict_customers(df, strategy)
    outreach = (
        results[results["selected"]]
        .sort_values("interest_score", ascending=False)
        .reset_index(drop=True)
    )
    # save these to use them later in app 
    st.session_state.campaign = {
        "file_name": uploaded_file.name,
        "uploaded_data": df,
        "strategy": strategy,
        "results": results,
        "outreach": outreach,
    }
    

# -----------------------------------
# Load a campaign
# -----------------------------------

campaign = st.session_state.campaign

if campaign is None:
    st.stop()

df = campaign["uploaded_data"]
results = campaign["results"]
outreach = campaign["outreach"]
strategy = campaign["strategy"]
    
# Create KPIs
metrics = calculate_dashboard_metrics(results, strategy)
reach = calculate_reach(df)

# --------------------------------------------------
# Campaign Recommendation
# --------------------------------------------------

st.write("")
st.markdown(
f"""
<div class="executive-card">

<div class="executive-title">
Executive Recommendation
</div>

<div class="executive-body">

Based on the selected <b>campaign objective</b>,
the AI recommends prioritizing 
<b>{metrics["customers_selected"]:,} customers for outreach.</b>
This audience is expected to generate approximately
<b>{metrics["expected_subscribers"]:,} subscriptions.</b>
</div>

</div>
""",
unsafe_allow_html=True
)

st.write("")

# --------------------------
# Recommendation + KPI Row
# --------------------------

    
st.subheader("Targeting Summary")
st.write("")


c1,c2,c3,c4 = st.columns(4)
with c1:
    with st.container(border=True):
        st.markdown("###### Customers Selected")
        st.markdown(
            f"<h3 style='margin:0'>{metrics['customers_selected']:,}</h3>",
            unsafe_allow_html=True,
            )
        st.caption("Recommended for outreach")
with c2:
    with st.container(border=True):
        st.markdown("###### Expected Conversions")
        st.markdown(
            f"<h3 style='margin:0'>{metrics['expected_subscribers']:,}</h3>",
            unsafe_allow_html=True,
            )
        st.caption("Likely to subscribe")         
with c3:
    efficiency = metrics["targeting_efficiency"]
    with st.container(border=True):
        st.markdown("###### Targeting Efficiency")
        st.markdown(
            f"<h3 style='margin:0'>{efficiency:.1%}</h3>",
            unsafe_allow_html=True,
            )
        st.caption("Expected conversion rate")
with c4:
    with st.container(border=True):
        st.markdown("###### Outreach Coverage")
        st.markdown(
            f"<h3 style='margin:0'>{metrics['outreach_coverage']:.1%}</h3>",
            unsafe_allow_html=True,
            )
        st.caption("Share of uploaded customers")
st.write("")
                            

# ------------------------
# Outreach Row
# ------------------------
st.subheader("Recommended Outreach List")   

# Keep only selected customers
outreach_list = outreach.copy()

# Rank
outreach_list.insert(0, "Rank", range(1, len(outreach_list) + 1))

# Convert probability to percentage
outreach_list["Subscription Probability"] = (
    outreach_list["interest_score"] * 100
).round(1).astype(str) + "%"

# Priority
def assign_priority(score):
    if score >= 0.90:
        return "High"
    elif score >= 0.75:
        return "Medium"
    else:
        return "Low"

outreach_list["Priority"] = outreach_list["interest_score"].apply(assign_priority)

# Summary
st.caption(
f"Showing the top 25 of {len(outreach_list):,} recommended customers "
"ranked by Subscription Probability.")

# --------------------------
# Filters
# --------------------------

filter_col1, filter_col2, filter_col3 = st.columns(3)

with filter_col1:
    priority_filter = st.selectbox(
        "Priority",
        ["All", "High", "Medium", "Low"]
    )

with filter_col2:
    job_filter = st.selectbox(
        "Job",
        ["All"] + sorted(outreach_list["job"].unique().tolist())
    )

with filter_col3:
    housing_filter = st.selectbox(
        "Housing Loan",
        ["All", "yes", "no"]
    )

# Apply filters
filtered_list = outreach_list.copy()

if priority_filter != "All":
    filtered_list = filtered_list[
        filtered_list["Priority"] == priority_filter
    ]

if job_filter != "All":
    filtered_list = filtered_list[
        filtered_list["job"] == job_filter
    ]

if housing_filter != "All":
    filtered_list = filtered_list[
        filtered_list["housing"] == housing_filter
    ]

# Display columns
display_columns = [
    "Rank",
    "age",
    "job",
    "balance",
    "housing",
    "Subscription Probability",
    "Priority",
]

# Display

st.dataframe(
    filtered_list[display_columns].head(25),
    use_container_width=True,
    height=450,
    hide_index=True,
)

csv_data = filtered_list.to_csv(index=False)

st.download_button(
"Export Outreach List",
csv_data,
"recommended_outreach_list.csv",
"text/csv")

