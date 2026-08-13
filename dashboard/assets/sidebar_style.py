import streamlit as st


def apply_sidebar_style():

    st.markdown("""
    <style>

    /* Sidebar */
    [data-testid="stSidebar"] {
        position: relative;
    }

    /* Product title */
    [data-testid="stSidebar"]::before {
        content: "Bank Customer Targeting";

        position: absolute;
        top: 1.5rem;
        left: 1rem;
        right: 1rem;

        font-family: inherit;
        font-size: 1.50rem;
        font-weight: 900;
        line-height: 1.3;

        color: #111827;

        padding: 2.0rem 0.5rem 2.2rem 0.5rem;
    }

    /* Product description */
    [data-testid="stSidebar"]::after {
        content: "AI-powered decision support for marketing outreach.";

        position: absolute;
        top: 4.0rem;
        left: 1rem;
        right: 1rem;

        font-family: inherit;
        font-size: 0.90rem;
        font-weight: 450;
        line-height: 1.45;

        color: #6B7280;

        padding: 2.5rem 0.5rem 2.2rem 0.5rem;
    }

    /* Automatic Streamlit navigation */
    [data-testid="stSidebarNav"] {
        padding-top: 6.0rem;
    }

    /* Navigation text */
    [data-testid="stSidebarNav"] span {
        font-size: 0.95rem;
    }

    </style>
    """, unsafe_allow_html=True)