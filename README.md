# Customer Subscription Prediction in Bank Marketing under Class Imbalance

> A machine learning project focused on handling class imbalance in real-world marketing data.

## Overview
This project focuses on predicting whether a client will subscribe to a term deposit using the Bank Marketing dataset. A key challenge is the strong class imbalance (~11.5% "yes"), which affects the model’s ability to correctly identify the minority class.

Several machine learning models and imbalance-handling techniques (Class Weighting, SMOTE, SMOTEENN) were explored and compared. The final model was selected based on performance, stability, and its ability to balance precision and recall.

---

## Objectives
- Compare multiple model families under class imbalance  
- Evaluate different imbalance-handling techniques (Class Weight, SMOTE, SMOTEENN)  
- Interpret model behavior using feature importance and SHAP  
- Align predictions with business objectives through threshold optimization   

---

## Models & Evaluation Approach
The following models were explored:

- XGBoost  
- Random Forest  
- Logistic Regression  
- SVM  

To ensure a fair comparison:
- A shared preprocessing pipeline was used to prevent data leakage  
- Stratified K-Fold cross-validation preserved class distribution  
- Multiple evaluation metrics were considered (Accuracy, Precision, Recall, F1, ROC-AUC, PR-AUC), with emphasis on precision, recall, and F1-score due to class imbalance. 

---

## Final Model Performance

The final selected model is **XGBoost with SMOTEENN**.

The model was initially developed and evaluated on a smaller subset of the data (4.5k records) for efficiency. It was then validated on the full dataset (45k records) to assess generalization.

| Dataset | Precision | Recall | F1-Score | PR-AUC |
| :--- | :--- | :--- | :--- | :--- |
| Experimental (4.5k) | 0.33 | 0.45 | 0.38 | 0.33 |
| **Full Validation (45k)** | **0.45** | **0.50** | **0.47** | **0.42** |

*Validation on the full dataset shows a clear improvement across all metrics, including an increase in F1-score from 0.38 to 0.47 (~24%), indicating that the model generalizes well and benefits from larger data.*

---

## Project Structure
The project is organized into multiple notebooks to separate experimentation, interpretation, and validation:

notebooks/01_exploratory_data_analysis Bank2.ipynb   # Data exploration and preprocessing checks  
notebooks/02_xgboost_evaluation.ipynb              # XGBoost experiments + model analysis and interpretation  
notebooks/03_rf_logreg_experiments.ipynb           # Random Forest and Logistic Regression experiments + RF interpretation  
notebooks/04_svm_experiment.ipynb                  # SVM experiments  
notebooks/05_xgboost_smoteenn_full_validation.ipynb # Final validation of the selected model (XGBoost + SMOTEENN) on the full dataset  

src/  
├── shared.py                       # Preprocessing pipeline and transformations  
└── evaluation.py                   # Cross-validation and evaluation metrics  

README.md

---

## Key Findings

- **Imbalance handling:** SMOTEENN consistently improved recall and overall F1-score, making it the most effective strategy for handling class imbalance.

- **Model performance:** XGBoost provided the most balanced results across metrics, achieving the best trade-off between precision and recall.

- **Important features:** Variables related to previous interactions and contact information (e.g., `poutcome`, `pdays`) had the strongest influence on predictions in XGBoost with SMOTEENN.

- **Decision strategy:** Adjusting the classification threshold improves practical performance, with lower thresholds helping to identify more potential subscribers compared to the default 0.5.

- **Model validation:** The final model maintained consistent performance on the full dataset and showed an improvement in F1-score, indicating good generalization.

---

## Setup & Requirements
- Python 3.x  
- Key libraries: `xgboost`, `imblearn`, `scikit-learn`, `shap`, `pandas`, `matplotlib`  
- Additional dependencies can be included in a `requirements.txt` file  
