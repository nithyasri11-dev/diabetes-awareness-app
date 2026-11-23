import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.inspection import permutation_importance


# Friendly names for the model features
FRIENDLY_NAMES = {
    "HighBP": "High Blood Pressure",
    "HighChol": "High Cholesterol",
    "BMI": "Body Mass Index (BMI)",
    "Smoker": "Smoking History",
    "Stroke": "History of Stroke",
    "HeartDiseaseorAttack": "Heart Disease or Heart Attack",
    "PhysActivity": "Physical Activity",
    "Fruits": "Fruit Consumption",
    "Veggies": "Vegetable Consumption",
    "HvyAlcoholConsump": "Heavy Alcohol Consumption",
    "GenHlth": "General Health",
    "PhysHlth": "Physical Health",
    "Age": "Age Group",
}


# Explanations for individual health factors
FACTOR_EXPLANATIONS = {
    "HighBP": (
        "Indicates whether the person reports having high blood pressure. "
        "This dataset feature is not a measured systolic or diastolic reading."
    ),
    "HighChol": (
        "Indicates whether the person reports having high cholesterol."
    ),
    "BMI": (
        "Body Mass Index is a measure based on height and weight. "
        "It is one of the health indicators considered by the model."
    ),
    "Smoker": (
        "Represents smoking history as recorded in the dataset."
    ),
    "Stroke": (
        "Represents a reported history of stroke."
    ),
    "HeartDiseaseorAttack": (
        "Represents a reported history of coronary heart disease or heart attack."
    ),
    "PhysActivity": (
        "Represents physical activity as recorded in the dataset."
    ),
    "Fruits": (
        "Represents fruit consumption as recorded in the dataset."
    ),
    "Veggies": (
        "Represents vegetable consumption as recorded in the dataset."
    ),
    "HvyAlcoholConsump": (
        "Represents heavy alcohol consumption according to the dataset definition."
    ),
    "GenHlth": (
        "Represents the person's self-reported general health."
    ),
    "PhysHlth": (
        "Represents the number of days of poor physical health reported "
        "within the dataset's specified period."
    ),
    "Age": (
        "Represents the age category recorded in the dataset."
    ),
}


def explainable_ai_page(model, features, data_path):
    """
    Display model-level feature importance.

    Parameters
    ----------
    model:
        The already-trained machine learning model.
    features:
        List of feature names used to train the model.
    data_path:
        Path to the dataset CSV file.
    """

    st.title("🧠 Explainable AI")
    st.subheader("Discover What Influences Your Model")

    st.write(
        "Explore the health factors used by the trained machine learning "
        "model and compare how they influence its performance."
    )

    st.info(
        "💡 The percentages displayed here represent relative feature "
        "importance. They are NOT percentages of an individual's diabetes risk."
    )

    # Check that the model and features are available
    if model is None:
        st.error("The trained model could not be loaded.")
        return

    if not features:
        st.error("No model features were provided.")
        return

    # Load the dataset
    try:
        df = pd.read_csv(data_path)
    except Exception as exc:
        st.error(f"Unable to load the dataset: {exc}")
        return

    target = "Diabetes_binary"

    # Check that all required columns exist
    required_columns = list(features) + [target]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        st.error(
            "The dataset is missing these required columns: "
            + ", ".join(missing_columns)
        )
        return

    # Keep only the columns needed for this analysis
    df = df[required_columns].dropna()

    if df.empty:
        st.error("No valid rows are available for analysis.")
        return

    # Use a reproducible sample to make analysis faster
    if len(df) > 2000:
        df = df.sample(n=2000, random_state=42)

    X = df[list(features)]
    y = df[target].astype(int)

    if y.nunique() < 2:
        st.error(
            "The selected dataset sample must contain both target classes."
        )
        return

    # Calculate permutation importance
    try:
        with st.spinner("🔍 Analysing health factors..."):
            result = permutation_importance(
                model,
                X,
                y,
                scoring="roc_auc",
                n_repeats=3,
                random_state=42,
                n_jobs=-1,
            )
    except Exception as exc:
        st.error(
            "Unable to calculate feature importance. "
            f"Check that the model and dataset features match. Details: {exc}"
        )
        return

    # Create the feature importance table
    importance_df = pd.DataFrame(
        {
            "Feature": list(features),
            "Importance": result.importances_mean,
            "Variation": result.importances_std,
        }
    )

    importance_df["Health Factor"] = (
        importance_df["Feature"]
        .map(FRIENDLY_NAMES)
        .fillna(importance_df["Feature"])
    )

    importance_df = (
        importance_df
        .sort_values("Importance", ascending=False)
        .reset_index(drop=True)
    )

    # --------------------------------------------------
    # TOP 5 HEALTH FACTORS
    # --------------------------------------------------

    st.divider()
    st.header("🏆 Top 5 Contributing Health Factors")

    st.write(
        "The highest positive importance score is used as the 100% "
        "reference. Other positive scores are displayed relative to it."
    )

    positive_scores = importance_df.loc[
        importance_df["Importance"] > 0,
        "Importance",
    ]

    if positive_scores.empty:
        max_score = None
        st.warning(
            "No positive importance scores were found for this sample. "
            "All relative importance percentages will be displayed as 0%."
        )
    else:
        max_score = float(positive_scores.max())

    top_factors = importance_df.head(5)

    for rank, (_, row) in enumerate(
        top_factors.iterrows(),
        start=1,
    ):
        feature = row["Feature"]
        name = row["Health Factor"]
        score = float(row["Importance"])

        # Calculate relative percentage
        if max_score is not None and score > 0:
            percentage = min(
                100.0,
                (score / max_score) * 100,
            )
        else:
            percentage = 0.0

        title_col, percentage_col = st.columns([4, 1])

        with title_col:
            st.markdown(f"### {rank}. {name}")

        with percentage_col:
            st.markdown(
                f"""
                <div style="
                    background: linear-gradient(135deg, #123B64, #167D9A);
                    color: white;
                    padding: 10px 5px;
                    border-radius: 12px;
                    text-align: center;
                    font-size: 20px;
                    font-weight: bold;
                    margin-top: 5px;
                ">
                    {percentage:.1f}%
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Progress bar
        st.progress(percentage / 100)

        st.caption(
            f"Relative importance: {percentage:.1f}% "
            "of the highest positive importance score"
        )

        st.markdown(
            f"**Feature importance score:** `{score:.4f}`"
        )

        # Show the health factor explanation
        explanation = FACTOR_EXPLANATIONS.get(
            feature,
            "This feature is included in the trained model.",
        )

        st.write(explanation)

        # Explanation card
        st.markdown(
            f"""
            <div style="
                background-color: #E8F5F9;
                color: #123B64;
                padding: 12px 15px;
                border-radius: 10px;
                border-left: 5px solid #167D9A;
                margin: 10px 0 18px 0;
            ">
                <b>📊 Relative Importance</b><br>
                {percentage:.1f}% compared with the highest
                positive importance score.
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.divider()

    # --------------------------------------------------
    # FEATURE IMPORTANCE COMPARISON CHART
    # --------------------------------------------------

    st.header("📈 Feature Importance Comparison")

    st.write(
        "Compare the importance scores of all health factors used "
        "by the model."
    )

    chart_df = importance_df.sort_values(
        "Importance",
        ascending=True,
    ).copy()

    fig = px.bar(
        chart_df,
        x="Importance",
        y="Health Factor",
        orientation="h",
        labels={
            "Importance": "Permutation Importance Score",
            "Health Factor": "Health Factor",
        },
        title="How Features Influence Model Performance",
        hover_data={
            "Feature": True,
            "Importance": ":.4f",
            "Variation": ":.4f",
        },
    )

    fig.update_layout(
        height=max(450, len(chart_df) * 38),
        showlegend=False,
        xaxis_title="Change in ROC-AUC after shuffling",
        yaxis_title="Health Factor",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    # --------------------------------------------------
    # ALL FEATURE SCORES
    # --------------------------------------------------

    with st.expander("📋 View All Health Factor Scores"):
        display_df = importance_df[
            ["Health Factor", "Importance", "Variation"]
        ].copy()

        display_df["Importance"] = display_df["Importance"].round(4)
        display_df["Variation"] = display_df["Variation"].round(4)

        display_df.columns = [
            "Health Factor",
            "Importance Score",
            "Score Variation",
        ]

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
        )

    # --------------------------------------------------
    # HOW TO INTERPRET RESULTS
    # --------------------------------------------------

    st.divider()
    st.header("💡 How to Understand These Results")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            #### 📊 Relative Importance

            - **100%** means the highest positive importance score.
            - **50%** means half of that reference score.
            - **0%** means the score is not positive.
            """
        )

    with col2:
        st.markdown(
            """
            #### 🧠 What It Means

            - Importance measures changes in model performance.
            - It does not prove that a factor causes diabetes.
            - It does not represent an individual's diabetes risk.
            """
        )

    st.warning(
        "A negative importance score is possible. It means that shuffling "
        "the feature did not reduce the measured performance on this sample. "
        "The percentage badge is set to 0% for non-positive scores, while "
        "the original score remains visible."
    )

    st.caption(
        "This analysis describes overall model behaviour on a sample of "
        "the dataset. It is not a medical diagnosis or a validated prediction "
        "of future diabetes."
    )