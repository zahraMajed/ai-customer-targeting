import streamlit as st
from pathlib import Path
import sys
from assets.sidebar_style import apply_sidebar_style
from production.explainability import (
    build_explainability_context,
    build_driver_breakdown,
    build_feature_importance_chart,
    build_driver_descriptions
)
import plotly.io as pio
pio.templates.default = "plotly_white"

# Get project root directory
ROOT_DIR = Path(__file__).resolve().parents[1]
# Add root directory to Python path
sys.path.append(str(ROOT_DIR))

st.set_page_config(
    page_title="AI-Powered Customer Targeting",
    layout="wide",
    initial_sidebar_state="collapsed"

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

st.title("Recommendation Explanation")
st.caption("Understand the factors that influenced the AI's recommendations.")
st.write("")

if "campaign" not in st.session_state:
    st.warning("No campaign has been generated yet.\n\nGo to **Decision Center** and generate a recommendation first.")
    st.stop()

campaign = st.session_state.campaign
results = campaign["results"]
outreach = campaign["outreach"]
strategy = campaign["strategy"]
df = campaign["uploaded_data"]

# Build explainability context
context = build_explainability_context(outreach)

# --------------------------------------------------
# Key Drivers
# --------------------------------------------------
st.markdown("#### Key Drivers")
st.caption("These factors had the strongest influence on the AI when selecting customers for outreach.")

with st.container(border=True):
    fig = build_feature_importance_chart(context)
    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )
    
st.markdown("#### Key Driver Details")
st.caption("The table highlights the customer characteristics most strongly associated with the AI's recommendations.")
driver_breakdown = build_driver_breakdown(context)

st.dataframe(
    driver_breakdown,
    use_container_width=True,
    hide_index=True
)
    
st.markdown("#### Why These Factors Matter")
st.caption("The explanations below describe why each customer characteristic is relevant when identifying potential subscribers.")

driver_descriptions = build_driver_descriptions()

st.dataframe(
    driver_descriptions,
    use_container_width=True,
    hide_index=True,
)