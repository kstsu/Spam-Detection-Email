"""Streamlit interface for the saved spam detector."""

import sys
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from spam_detection.features import (
    text_to_features,
    validate_feature_frame,
)

MODEL_PATH = PROJECT_ROOT / "models" / "spam_detector.joblib"
METADATA_PATH = PROJECT_ROOT / "models" / "training_metadata.json"


@st.cache_resource
def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            "The trained model is not available. Run python -m spam_detection.train first."
        )
    return joblib.load(MODEL_PATH)


def predict(features: pd.DataFrame) -> tuple[str, float | None]:
    """Predict one or more validated feature rows."""
    model = load_model()
    labels = model.predict(features)
    probabilities = (
        model.predict_proba(features)[:, 1] if hasattr(model, "predict_proba") else None
    )
    label = "spam" if int(labels[0]) == 1 else "not_spam"
    probability = float(probabilities[0]) if probabilities is not None else None
    return label, probability


st.set_page_config(page_title="Spam Detection Email", page_icon="✉️")
st.title("Spam Detection Email")
st.write("Classify a message using the saved traditional machine-learning pipeline.")
st.caption("Model used: Random Forest")

if not MODEL_PATH.exists():
    st.warning(
        "No trained model is available yet. Run the training command from the README."
    )
else:
    mode = st.radio(
        "Input method", ("Paste email text", "Upload feature CSV"), horizontal=True
    )
    features = None
    if mode == "Paste email text":
        text = st.text_area(
            "Email text", height=220, placeholder="Paste the email message here"
        )
        if st.button("Classify email", type="primary"):
            try:
                features = text_to_features(text)
            except ValueError as error:
                st.error(str(error))
    else:
        upload = st.file_uploader(
            "CSV with the 57 Spambase feature columns", type="csv"
        )
        if upload is not None and st.button("Classify CSV", type="primary"):
            try:
                features = validate_feature_frame(pd.read_csv(upload))
            except (ValueError, pd.errors.ParserError) as error:
                st.error(f"Invalid CSV: {error}")

    if features is not None:
        try:
            label, probability = predict(features)
            st.subheader(f"Prediction: {label}")
            if probability is not None:
                st.metric("Spam probability", f"{probability:.1%}")
            st.caption(
                "The model uses the 57 numeric Spambase features. Text extraction is an approximation because the original email corpus is unavailable."
            )
        except (KeyError, RuntimeError, TypeError, ValueError) as error:  # pragma: no cover
            st.error(f"Prediction failed: {error}")

st.divider()
st.caption(
    "Spam is the positive class. A false positive can hide a legitimate email; use this result as a second opinion."
)
