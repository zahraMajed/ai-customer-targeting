import sys
from pathlib import Path
import textwrap

import streamlit as st
from assets.sidebar_style import apply_sidebar_style


# ─────────────────────────────────────────────
# PROJECT ROOT
# ─────────────────────────────────────────────

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))


# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="AI-Powered Customer Targeting",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ─────────────────────────────────────────────
# LOAD CSS
# ─────────────────────────────────────────────

css_file = ROOT_DIR / "dashboard" / "assets" / "styles.css"

with open(css_file, encoding="utf-8") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

apply_sidebar_style()


# ─────────────────────────────────────────────
# HERO
# ─────────────────────────────────────────────

st.title("Bank Customer Targeting")

st.caption(
    "AI-powered decision support for bank marketing outreach."
)
st.write("")


# ─────────────────────────────────────────────
# WHAT THE PRODUCT DOES
# ─────────────────────────────────────────────
st.markdown("#### What the product does")

st.html("""
<div class="product-card">

    <div class="product-capability">
        <div class="capability-number">01</div>
        <div class="capability-content">
            <strong>Prioritize</strong>
            <span>Identify customers to prioritize for outreach based on the selected campaign objective.</span>
        </div>
    </div>

    <div class="product-capability">
        <div class="capability-number">02</div>
        <div class="capability-content">
            <strong>Explain</strong>
            <span>Understand the key factors behind the recommendations.</span>
        </div>
    </div>

    <div class="product-capability">
        <div class="capability-number">03</div>
        <div class="capability-content">
            <strong>Profile</strong>
            <span>Explore the characteristics of the recommended customers.</span>
        </div>
    </div>

</div>
""")

# ─────────────────────────────────────────────
# HOW IT WORKS
# ─────────────────────────────────────────────

st.markdown("#### How it works")


st.html("""
<div class="workflow">

    <div class="workflow-step">
        <div class="workflow-number">01</div>
        <h5>Upload Customer Data</h5>
        <p>Provide customer data using the required input structure.</p>
    </div>

    <div class="workflow-arrow">→</div>

    <div class="workflow-step">
        <div class="workflow-number">02</div>
        <h5>Choose Campaign Objective</h5>
        <p>Select how broad or selective the outreach should be.</p>
    </div>

    <div class="workflow-arrow">→</div>

    <div class="workflow-step">
        <div class="workflow-number">03</div>
        <h5>Review Recommended Customers</h5>
        <p>Explore the prioritized customers and audience insights.</p>
    </div>

</div>
""")

# ─────────────────────────────────────────────
# START
# ─────────────────────────────────────────────


if st.button(
    "Start Customer Targeting  →",
    type="primary"
):
    st.switch_page("pages/Customer_Targeting.py")