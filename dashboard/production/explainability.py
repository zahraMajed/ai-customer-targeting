from pathlib import Path
import joblib
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
import pandas as pd



# --------------------------------------------------
# Paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

MODEL_PATH = BASE_DIR / "models" / "xgb_smoteenn_pipeline.pkl"
EXPLAINER_PATH = BASE_DIR / "models" / "shap_explainer.pkl"
FEATURE_NAMES_PATH = BASE_DIR / "models" / "feature_names.pkl"

# --------------------------------------------------
# Load artifacts (loaded once)
# --------------------------------------------------

pipeline = joblib.load(MODEL_PATH)
explainer = joblib.load(EXPLAINER_PATH)
feature_names = joblib.load(FEATURE_NAMES_PATH).tolist()

# --------------------------------------------------
# Prepare data exactly as during training
# --------------------------------------------------
def prepare_data(df):
    X = pipeline.named_steps["drop_columns"].transform(df)
    X = pipeline.named_steps["pdays_transform"].transform(X)
    X = pipeline.named_steps["preprocessor"].transform(X)
    if hasattr(X, "toarray"):
        X = X.toarray()
    return X

# This converts the encoded feature names into high-level business concepts.

FEATURE_GROUPS = {
    # Customer profile
    "num__age": "Age",
    "cat__job": "Occupation",
    "cat__education": "Education",
    "cat__marital": "Marital Status",

    # Financial profile
    "num__balance": "Account Balance",
    "cat__housing": "Housing Loan",
    "cat__loan": "Personal Loan",

    # Campaign history
    "num__campaign": "Current Campaign Contacts",
    "num__pdays": "Days Since Previous Contact",
    "num__previous": "Number of Previous Contacts",
    "cat__poutcome": "Previous Campaign Outcome",

    # Current campaign
    "cat__contact": "Contact Method",
    "cat__month": "Contact Month",
    "cat__day": "Contact Day",
}

# Convert one-hot encoded feature names into high-level business concepts.
# Examples: cat__month_oct -> Contact Month
def get_feature_group(feature):
    
    # Numerical features are already complete names. such as num__balance
    # We simply look them up in FEATURE_GROUPS.
    if feature.startswith("num__"):
        return FEATURE_GROUPS.get(feature, None)
    
    # One-hot encoded categorical features contain both the feature name and its value. such as cat__job_retired
    # We only need: cat__job because every job category belongs to the same business concept: Occupation.
    if feature.startswith("cat__"):
        # Remove "cat__"
        feature = feature.replace("cat__", "")
        # Extract only the original feature name
        group = feature.split("_", 1)[0]
        return FEATURE_GROUPS.get( f"cat__{group}", group.title())
    
    return feature

# --------------------------------------------------
# explainability essential functions
# --------------------------------------------------
def compute_shap_values(df):
    X = prepare_data(df)
    shap_values = explainer(X)
    return shap_values, X

def build_explainability_context(df):
    shap_values, X = compute_shap_values(df)
    
    return {
        "data": df,
        "X": X,
        "shap_values": shap_values,
        "driver_importance": None
    }


# Calculate the overall importance of each business concept using SHAP values.
def build_grouped_feature_importance(context):

    shap_values = context["shap_values"]
    # since SHAP values can be positive (pushes prediction towards subscribing) or negative.
    # We are interested in the positive
    positive_importance = np.maximum(shap_values.values, 0).mean(axis=0)
    
    # Create a table containing: Feature name and Average positive SHAP importance
    importance_df = pd.DataFrame({
        "Feature": feature_names,
        "Importance": positive_importance
    })
    
    # Replace one-hot encoded feature names with high-level business concepts.
    importance_df["Group"] = (importance_df["Feature"].apply(get_feature_group))
    
    # Remove engineered features that are not intended to be shown in the dashboard.
    importance_df = importance_df.dropna(subset=["Group"])
    
    # Multiple encoded columns can belong to the same business concept. EX: month_jan,  month_feb
    # We avg their importance to obtain the overall importance of Contact Month.
    importance_df = (importance_df.groupby("Group", as_index=False)["Importance"].mean())

    # Show only the most influential business concepts.
    importance_df = (
        importance_df
        .sort_values("Importance", ascending=False))
    context["driver_importance"] = importance_df 

    return importance_df


def build_feature_importance_chart(context):
    
    importance_df = build_grouped_feature_importance(context)

    fig = px.bar(
        importance_df,
        x="Importance",
        y="Group",
        orientation="h",
    )
    
    colors = [
            "#2563EB",  # 1st
            "#3B82F6",  # 2nd
            "#60A5FA",# 3rd
            "#93C5FD"
        ]
    # All remaining bars use the same light cyan.
    colors.extend(["#BFDBFE"] * (len(importance_df) - 3))

    fig.update_traces(
        marker_color=colors,
        marker_line_width=0,
    )

    fig.update_layout(
        yaxis=dict(categoryorder="total ascending"),
        xaxis_title="Contribution to Recommendation",
        yaxis_title="",
        height=420,
        margin=dict(l=20, r=20, t=20, b=20),
        bargap=0.1
    )

    return fig

# --------------------------------------------------
# Metadata describing each business driver.
#
# This metadata is used to:
#
# 1. Locate the original dataframe column.
# 2. Identify whether the driver is categorical or numeric.
# 3. Find the corresponding encoded SHAP features.
# 4. Provide a business explanation.
# --------------------------------------------------

FEATURE_METADATA = {

    "Contact Month": {
        "column": "month",
        "encoded_prefix": "cat__month_",
        "type": "categorical",
        "description":"Customers contacted during certain months were historically more likely to subscribe."
    },

    "Contact Day": {
        "column": "day",
        "encoded_prefix": "cat__day_",
        "type": "categorical",
        "description": "The timing of customer contact during the month influenced campaign success."
    },

    "Occupation": {
        "column": "job",
        "encoded_prefix": "cat__job_",
        "type": "categorical",
        "description":"Certain occupations responded more positively to previous marketing campaigns."
    },

    "Education": {
        "column": "education",
        "encoded_prefix": "cat__education_",
        "type": "categorical",
        "description": "Customers with different education levels showed different subscription patterns."
    },

    "Marital Status": {
        "column": "marital",
        "encoded_prefix": "cat__marital_",
        "type": "categorical",
        "description": "Subscription behaviour varied across marital status groups."
    },

    "Housing Loan": {
        "column": "housing",
        "encoded_prefix": "cat__housing_",
        "type": "categorical",
        "description": "Housing loan status was associated with different subscription behaviour."
    },

    "Personal Loan": {
        "column": "loan",
        "encoded_prefix": "cat__loan_",
        "type": "categorical",
        "description": "Personal loan status provided additional information about customer behaviour."
    },

    "Previous Campaign Outcome": {
        "column": "poutcome",
        "encoded_prefix": "cat__poutcome_",
        "type": "categorical",
        "description": "Customers who responded differently in previous campaigns tended to behave differently in future campaigns."
    },

    "Contact Method": {
        "column": "contact",
        "encoded_prefix": "cat__contact_",
        "type": "categorical",
        "description": "The communication channel influenced customer response rates."
    },

    "Age": {
        "column": "age",
        "encoded_feature": "num__age",
        "type": "numeric",
        "description":"Customer age helped distinguish groups with different subscription behaviour."
    },

    "Account Balance": {
        "column": "balance",
        "encoded_feature": "num__balance",
        "type": "numeric",
        "description": "Account balance reflected different levels of customer engagement."
    },

    "Current Campaign Contacts": {
        "column": "campaign",
        "encoded_feature": "num__campaign",
        "type": "numeric",
        "description": "The number of contacts during the current campaign influenced the likelihood of a successful response."
    },

    "Days Since Previous Contact": {
        "column": "pdays",
        "encoded_feature": "num__pdays",
        "type": "numeric",
        "description": "The time since the previous customer contact affected customer responsiveness."
    },

    "Number of Previous Contacts": {
        "column": "previous",
        "encoded_feature": "num__previous",
        "type": "numeric",
        "description": "Previous customer interactions provided additional context for future recommendations."
    }

}

# --------------------------------------------------
# Driver Breakdown
# For each important business driver, identify the specific values that contributed most positively to the AI's recommendations.
# Example:
# Driver: Contact Month. Instead of showing only: Contact Month. We want: October, March
# --------------------------------------------------

def build_driver_breakdown(context):

    df = context["data"]
    shap_values = context["shap_values"]

    # Retrieve the top business drivers from the previous chart.
    driver_importance = context["driver_importance"]

    breakdown = []
    
    # For each driver read its metadata
    for _, row in driver_importance.iterrows():
        # get the driver 
        driver = row["Group"]
        # get its metadata
        info = FEATURE_METADATA[driver]

        # If categorical:
        if info["type"] == "categorical":
            
            # 1. Find all SHAP columns with encoded_prefix.
            # Example: Contact Month -> cat__month_jan, cat__month_feb
            encoded_columns = []
            for i, feature in enumerate(feature_names):
                if feature.startswith(info["encoded_prefix"]):
                    encoded_columns.append((i, feature))
            
            # 2. Rank the categories by average positive SHAP.
            values = []
            for idx, feature in encoded_columns:
                # Take all rows in shap table, but only feature's column by idk (which is ).
                # np.maximum(a, b) compares every element with 0 and keeps the larger one (to get the positive only)
                positive_score = np.maximum(shap_values.values[:, idx],0).mean()
                # get the value only without the encoded_prefix
                value = (
                    feature
                    .replace(info["encoded_prefix"], "")
                    .replace("_", " ")
                    .title())
                values.append((value, positive_score))
                
            # 3. Return the top 3 values (e.g., October, March).
            values.sort(key=lambda x: x[1],reverse=True)
            top_values = ", ".join(value for value, _ in values[:3])

        #If numeric:
        
        else:
            # 1. Find the corresponding SHAP feature.
            feature_index = feature_names.index(info["encoded_feature"])
            # 2. Look at customers where that SHAP value is positive.
            positive_rows = (shap_values.values[:, feature_index] > 0)

            positive_data = df.loc[
                positive_rows,
                info["column"]]

            if len(positive_data) == 0:
                top_values = "Not available"
            else:
                q1 = positive_data.quantile(0.25)
                median = positive_data.median()
                q3 = positive_data.quantile(0.75)
            
                # Add business-friendly units depending on
                # the feature being described.
                if driver == "Age":
                    top_values = (
                        f"Typically {q1:.0f}-{q3:.0f} years "
                        f"(median {median:.0f})"
                    )

                elif driver == "Current Campaign Contacts":
                    top_values = (
                        f"Typically {q1:.0f}-{q3:.0f} contacts "
                        f"(median {median:.0f})"
                    )

                elif driver == "Days Since Previous Contact":
                    top_values = (
                        f"Typically {q1:.0f}-{q3:.0f} days "
                        f"(median {median:.0f})"
                    )

                elif driver == "Account Balance":
                    top_values = (
                        f"Typically {q1:,.0f}-{q3:,.0f} "
                        f"(median {median:,.0f})"
                    )
                    
                else:
                    top_values = (
                        f"Typically {q1:.0f}-{q3:.0f} "
                        f"(median {median:.0f})"
                    )

        breakdown.append({
            "Driver": driver,
            "Most Influential Values": top_values})

    return pd.DataFrame(breakdown)

def build_driver_descriptions():

    explanations = []

    for driver, info in FEATURE_METADATA.items():

        explanations.append({
            "Driver": driver,
            "Why It Matters": info["description"]})

    return pd.DataFrame(explanations)