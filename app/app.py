import streamlit as st
import pandas as pd
import pickle

# ==========================
# LOAD MODEL
# ==========================

model = pickle.load(open("fraud_model.pkl", "rb"))

# ==========================
# PAGE CONFIG
# ==========================

st.set_page_config(
    page_title="Financial Fraud Detection",
    page_icon="💳",
    layout="wide"
)

st.title("💳 Financial Fraud Detection System")

st.markdown(
"""
Detect fraudulent credit card transactions using Machine Learning.

Models Used:
- Logistic Regression
- Random Forest
- XGBoost
- SMOTE
"""
)

# ==========================
# TABS
# ==========================

tab1, tab2, tab3 = st.tabs(
    [
        "📊 Dashboard Summary",
        "🔍 Manual Prediction",
        "📂 CSV Upload Prediction"
    ]
)

# ==================================================
# TAB 1 : DASHBOARD
# ==================================================

with tab1:

    st.subheader("Project Overview")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Transactions",
            "284,807"
        )

    with col2:
        st.metric(
            "Fraud Transactions",
            "492"
        )

    with col3:
        st.metric(
            "Fraud Rate",
            "0.17%"
        )

    st.markdown("---")

    st.subheader("Model Performance")

    result_df = pd.DataFrame({
        "Model": [
            "Logistic Regression",
            "Random Forest",
            "XGBoost"
        ],
        "Accuracy": [
            "97%",
            "99.95%",
            "99.93%"
        ],
        "Recall": [
            "81%",
            "76.84%",
            "80%"
        ],
        "F1 Score": [
            "75%",
            "82.49%",
            "80.42%"
        ]
    })

    st.dataframe(result_df)

    st.markdown("---")

    st.subheader("Top Important Features")

    feature_df = pd.DataFrame({
        "Feature": [
            "V14",
            "V12",
            "V4",
            "V17",
            "V8"
        ]
    })

    st.dataframe(feature_df)

    st.markdown("---")

    st.subheader("Business Impact")

    st.markdown(
    """
    ✅ Early Fraud Detection

    ✅ Reduced Financial Losses

    ✅ Improved Customer Trust

    ✅ Automated Monitoring

    ✅ Better Risk Management
    """
    )

# ==================================================
# TAB 2 : MANUAL PREDICTION
# ==================================================

with tab2:

    st.subheader("Manual Fraud Prediction")

    amount = st.number_input(
        "Transaction Amount",
        value=100.0
    )

    v14 = st.number_input(
        "V14",
        value=0.0
    )

    v12 = st.number_input(
        "V12",
        value=0.0
    )

    v4 = st.number_input(
        "V4",
        value=0.0
    )

    v17 = st.number_input(
        "V17",
        value=0.0
    )

    v8 = st.number_input(
        "V8",
        value=0.0
    )

    if st.button("Predict Fraud Risk"):

        sample = pd.DataFrame([{

            "Time": 0,

            "V1": 0,
            "V2": 0,
            "V3": 0,

            "V4": v4,

            "V5": 0,
            "V6": 0,
            "V7": 0,

            "V8": v8,

            "V9": 0,
            "V10": 0,
            "V11": 0,

            "V12": v12,

            "V13": 0,

            "V14": v14,

            "V15": 0,
            "V16": 0,

            "V17": v17,

            "V18": 0,
            "V19": 0,
            "V20": 0,
            "V21": 0,
            "V22": 0,
            "V23": 0,
            "V24": 0,
            "V25": 0,
            "V26": 0,
            "V27": 0,
            "V28": 0,

            "Amount": amount

        }])

        prediction = model.predict(sample)[0]

        probability = model.predict_proba(sample)[0][1]

        st.write(
            f"Fraud Probability: {probability*100:.2f}%"
        )

        if prediction == 1:

            st.error(
                "⚠ Fraud Transaction Detected"
            )

        else:

            st.success(
                "✅ Normal Transaction"
            )

# ==================================================
# TAB 3 : CSV UPLOAD
# ==================================================

with tab3:

    st.subheader("Upload CSV File")

    uploaded_file = st.file_uploader(
        "Upload CSV",
        type=["csv"]
    )

    if uploaded_file is not None:

        df = pd.read_csv(uploaded_file)

        st.write("Uploaded Data")

        st.dataframe(df.head())

        try:

            if "Class" in df.columns:

                df = df.drop(
                    "Class",
                    axis=1
                )

            predictions = model.predict(df)

            df["Prediction"] = predictions

            fraud_count = (
                df["Prediction"] == 1
            ).sum()

            normal_count = (
                df["Prediction"] == 0
            ).sum()

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "Fraud Transactions",
                    int(fraud_count)
                )

            with col2:

                st.metric(
                    "Normal Transactions",
                    int(normal_count)
                )

            st.success(
                "Prediction Completed Successfully"
            )

            st.subheader(
                "Prediction Results"
            )

            st.dataframe(
                df.head(20)
            )

            fraud_df = df[
                df["Prediction"] == 1
            ]

            st.subheader(
                "Detected Fraud Transactions"
            )

            if len(fraud_df) > 0:

                st.dataframe(
                    fraud_df
                )

            else:

                st.success(
                    "No Fraud Transactions Detected"
                )

            csv = df.to_csv(
                index=False
            )

            st.download_button(
                "📥 Download Results",
                csv,
                "fraud_predictions.csv",
                "text/csv"
            )

        except Exception as e:

            st.error(
                f"Error: {e}"
            )