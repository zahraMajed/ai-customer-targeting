import streamlit as st


def apply_sidebar_style():

    st.markdown("""
    <style>

    /* =========================
       SIDEBAR
       ========================= */

    [data-testid="stSidebar"] {
        position: relative;
    }


    /* =========================
       PRODUCT TITLE
       ========================= */

    [data-testid="stSidebar"]::before {
        content: "Bank Customer Targeting";

        position: absolute;
        top: 1.2rem;
        left: 1.2rem;
        right: 1.2rem;

        font-family: inherit;
        font-size: clamp(1.2rem, 1.7vw, 1.5rem);
        font-weight: 900;
        line-height: 1.25;

        color: #111827;

        white-space: normal;
        overflow-wrap: break-word;
    }


    /* =========================
       PRODUCT DESCRIPTION
       ========================= */

    [data-testid="stSidebar"]::after {
        content: "AI-powered decision support for marketing outreach.";

        position: absolute;
        top: 5.2rem;
        left: 1.2rem;
        right: 1.2rem;

        font-family: inherit;
        font-size: clamp(0.78rem, 1vw, 0.9rem);
        font-weight: 450;
        line-height: 1.4;

        color: #6B7280;

        white-space: normal;
        overflow-wrap: break-word;
    }


    /* =========================
       AUTOMATIC STREAMLIT NAVIGATION
       ========================= */

    [data-testid="stSidebarNav"] {
        padding-top: 7.8rem;
    }


    /* Navigation text */

    [data-testid="stSidebarNav"] span {
        font-size: 0.95rem;
    }


    /* =========================
       SMALL SCREENS
       ========================= */

    @media (max-width: 700px) {

        [data-testid="stSidebar"]::before {
            top: 1rem;
            left: 1rem;
            right: 1rem;
            font-size: 1.25rem;
        }

        [data-testid="stSidebar"]::after {
            top: 4.6rem;
            left: 1rem;
            right: 1rem;
            font-size: 0.8rem;
        }

        [data-testid="stSidebarNav"] {
            padding-top: 7rem;
        }
    }

    </style>
    """, unsafe_allow_html=True)