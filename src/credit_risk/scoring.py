import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    roc_auc_score,
    precision_score,
    recall_score,
    confusion_matrix,
)
import joblib
from config.settings import MODELS_DIR

FEATURES = [
    "leverage_ratio",
    "interest_coverage",
    "current_ratio",
    "revenue_growth",
    "years_in_business",
    "has_collateral",
]


def train_credit_model(df: pd.DataFrame, save_model: bool = True):
    """
    Trains a Logistic Regression model to predict Probability of Default (PD).
    """
    X = df[FEATURES]
    y = df["default"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    pipeline = Pipeline(
        [
            ("scaler", StandardScaler()),
            (
                "classifier",
                LogisticRegression(
                    class_weight="balanced", random_state=42, max_iter=1000
                ),
            ),
        ]
    )

    pipeline.fit(X_train, y_train)

    # Evaluate
    y_pred = pipeline.predict(X_test)
    y_prob = pipeline.predict_proba(X_test)[:, 1]

    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "roc_auc": roc_auc_score(y_test, y_prob),
        "precision": precision_score(y_test, y_pred),
        "recall": recall_score(y_test, y_pred),
        "confusion_matrix": confusion_matrix(y_test, y_pred).tolist(),
    }

    if save_model:
        model_path = MODELS_DIR / "credit_model.pkl"
        joblib.dump(pipeline, model_path)

    return pipeline, metrics


def predict_default_probability(model_pipeline, df: pd.DataFrame) -> pd.Series:
    """Predicts PD for given borrowers."""
    X = df[FEATURES]
    pd_scores = model_pipeline.predict_proba(X)[:, 1]
    return pd.Series(pd_scores, index=df.index)


def assign_credit_rating(pd_score: float) -> str:
    """Maps Probability of Default to a synthetic Credit Rating."""
    if pd_score < 0.005:
        return "AAA"
    elif pd_score < 0.01:
        return "AA"
    elif pd_score < 0.02:
        return "A"
    elif pd_score < 0.04:
        return "BBB"
    elif pd_score < 0.08:
        return "BB"
    elif pd_score < 0.15:
        return "B"
    elif pd_score < 0.25:
        return "CCC"
    else:
        return "D"
