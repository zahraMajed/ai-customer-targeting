# This pages load the trained model and make predictions for new customers.


import joblib
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parents[2]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))
MODEL_PATH = BASE_DIR / "models" / "xgb_smoteenn_pipeline.pkl"
strategy_config_PATH = BASE_DIR / "models" / "strategy_config.pkl"

# Load trained pipeline
model = joblib.load(MODEL_PATH)
# Load thresholds dictionary
strategy_config=joblib.load(strategy_config_PATH)

# Predict_customers returns a copy of the uploaded data with two additional columns:
# 'interest_score' (predicted probability of customer subscription)
# and 'selected' (indicates whether the customer is selected based on the threshold)
def predict_customers(data, strategy):

    """
    data:
        uploaded customer dataframe

    strategy:
        Aggressive
        Balanced
        Conservative
    """

    # Get threshold for chosen strategy
    threshold = strategy_config[strategy]["threshold"]
    # Predict probability of subscription only (the positive class only)
    probabilities = model.predict_proba(data)[:,1]
    # Decide who gets selected
    selected = probabilities >= threshold

    # Copy uploaded data
    results = data.copy()
    # Add probability score
    results["interest_score"] = probabilities
    # Add selection decision
    results["selected"] = selected

    return results