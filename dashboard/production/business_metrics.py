# Generate the KPI cards for the dashboard.

import joblib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
strategy_config_PATH = BASE_DIR / "models" / "strategy_config.pkl"
strategy_config=joblib.load(strategy_config_PATH)

def calculate_dashboard_metrics(results,strategy):

    """
    Create values shown in dashboard KPI cards
    """

    # Keep only selected customers
    selected = results[results["selected"]]
    
    # --------------------------
    # KPI 1
    # --------------------------
    customers_selected = len(selected)
    # --------------------------
    # KPI 3
    # --------------------------
    targeting_efficiency = strategy_config[strategy]["targeting_efficiency"]
    # --------------------------
    # KPI 2
    # --------------------------
    expected_subscribers= likely_subscribers = round(selected["interest_score"].sum())
    # --------------------------
    # KPI 4
    # --------------------------
    outreach_coverage = (customers_selected / len(results))

    return {
        "customers_selected":
            customers_selected,
        "expected_subscribers":
            expected_subscribers,
        "targeting_efficiency":
            targeting_efficiency,
        "outreach_coverage":
            outreach_coverage
    }