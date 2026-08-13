import joblib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

CONFIG_PATH = BASE_DIR / "models" / "strategy_config.pkl"
MODEL_PATH = BASE_DIR / "models" / "xgb_smoteenn_pipeline.pkl"

model = joblib.load(MODEL_PATH)
strategy_config = joblib.load(CONFIG_PATH)


def calculate_reach(data):

    probabilities = model.predict_proba(data)[:, 1]

    reach = {}

    for strategy, config in strategy_config.items():

        threshold = config["threshold"]

        selected = probabilities >= threshold

        reach[strategy] = { "threshold": threshold, 
                           "customers_selected": selected.sum(),
                           "coverage":selected.sum()/ len(probabilities)}

    return reach