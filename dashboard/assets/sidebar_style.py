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
        top: 3.0rem;
        left: 1rem;
        right: 1rem;

        font-family: inherit;
        font-size: 1.35rem;
        font-weight: 900;
        line-height: 1.3;

        color: #111827;

        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    /* Product description */
    [data-testid="stSidebar"]::after {
        content: "AI-powered decision support for marketing outreach.";

        position: absolute;
        top: 5.0rem;
        left: 1rem;
        right: 1rem;

        font-family: inherit;
        font-size: 0.90rem;
        font-weight: 450;
        line-height: 1.45;

        color: #6B7280;
    }

    /* Automatic Streamlit navigation */
    [data-testid="stSidebarNav"] {
        padding-top: 5.8rem;
    }

    /* Navigation text */
    [data-testid="stSidebarNav"] span {
        font-size: 1.0rem;
    }

    </style>
    """, unsafe_allow_html=True)