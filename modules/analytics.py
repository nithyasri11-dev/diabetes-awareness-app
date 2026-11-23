from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


def render_analytics(results_path, data_path):

    # =====================================================
    # PAGE HEADER
    # =====================================================

    st.title("💙 Your Health Insights")

    st.write(
        "Understand general health patterns and discover "
        "simple ways to support your well-being."
    )

    st.info(
        "These insights describe patterns in a public dataset. "
        "They do not determine your personal diabetes risk."
    )

    # =====================================================
    # LOAD DATASET
    # =====================================================

    data_path = Path(data_path)

    if not data_path.exists():

        st.error(
            "The health dataset could not be found. "
            "Please check your data folder."
        )

        return

    try:

        df = pd.read_csv(data_path)

    except Exception as error:

        st.error(
            f"Unable to load the health dataset: {error}"
        )

        return

    # =====================================================
    # SIMPLE OVERVIEW CARDS
    # =====================================================

    st.subheader("📊 Health Information at a Glance")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "People in Dataset",
            f"{len(df):,}",
        )

    with col2:

        st.metric(
            "Health Indicators",
            len(df.columns) - 1
            if "Diabetes_binary" in df.columns
            else len(df.columns),
        )

    with col3:

        st.metric(
            "Topics Explored",
            "4",
        )

    st.caption(
        "These numbers describe the source dataset, "
        "not your individual health."
    )

    st.divider()

    # =====================================================
    # GENERAL HEALTH PATTERNS
    # =====================================================

    st.header("🔎 Explore Health Patterns")

    st.write(
        "Choose a topic to explore information recorded "
        "in the public dataset."
    )

    available_topics = {}

    if "BMI" in df.columns:

        available_topics["Body Mass Index (BMI)"] = "BMI"

    if "HighBP" in df.columns:

        available_topics["High Blood Pressure"] = "HighBP"

    if "HighChol" in df.columns:

        available_topics["High Cholesterol"] = "HighChol"

    if "PhysActivity" in df.columns:

        available_topics["Physical Activity"] = "PhysActivity"

    if not available_topics:

        st.warning(
            "No supported health indicators were found."
        )

        return

    selected_topic = st.selectbox(
        "What would you like to explore?",
        list(available_topics.keys()),
    )

    selected_column = available_topics[selected_topic]

    # -----------------------------------------------------
    # BMI CHART
    # -----------------------------------------------------

    if selected_column == "BMI":

        bmi_data = pd.to_numeric(
            df["BMI"],
            errors="coerce",
        ).dropna()

        bmi_data = bmi_data[
            (bmi_data >= 10)
            & (bmi_data <= 80)
        ]

        if bmi_data.empty:

            st.warning(
                "There is no usable BMI information to display."
            )

        else:

            chart_df = pd.DataFrame({
                "BMI": bmi_data
            })

            fig = px.histogram(
                chart_df,
                x="BMI",
                nbins=25,
                title="Body Mass Index Across the Dataset",
                labels={
                    "BMI": "Body Mass Index",
                    "count": "Number of records",
                },
            )

            fig.update_layout(
                showlegend=False,
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
            )

            st.markdown("### What does this mean?")

            st.write(
                "BMI compares weight with height. This chart shows "
                "how BMI values are distributed among records in "
                "the dataset."
            )

            st.info(
                "BMI is only a screening measure. It cannot diagnose "
                "diabetes or describe a person's entire health."
            )

    # -----------------------------------------------------
    # BINARY HEALTH INDICATORS
    # -----------------------------------------------------

    else:

        indicator_labels = {
            "HighBP": (
                "Reported high blood pressure",
                "This chart summarizes whether people reported "
                "a history of high blood pressure."
            ),
            "HighChol": (
                "Reported high cholesterol",
                "This chart summarizes whether people reported "
                "a history of high cholesterol."
            ),
            "PhysActivity": (
                "Reported physical activity",
                "This chart summarizes reported physical activity "
                "in the source dataset."
            ),
        }

        yes_label, description = indicator_labels[
            selected_column
        ]

        values = pd.to_numeric(
            df[selected_column],
            errors="coerce",
        ).dropna()

        counts = values.value_counts().reindex(
            [0, 1],
            fill_value=0,
        )

        chart_df = pd.DataFrame({
            "Response": [
                "No",
                "Yes",
            ],
            "Records": [
                int(counts.loc[0]),
                int(counts.loc[1]),
            ],
        })

        fig = px.bar(
            chart_df,
            x="Response",
            y="Records",
            text="Records",
            title=yes_label,
            labels={
                "Response": "Reported response",
                "Records": "Number of records",
            },
        )

        fig.update_layout(
            showlegend=False,
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

        st.markdown("### What does this mean?")

        st.write(description)

        st.caption(
            "These results describe the source dataset. "
            "They do not establish the cause of diabetes."
        )

    st.divider()

    # =====================================================
    # DATASET CLASS DISTRIBUTION
    # =====================================================

    if "Diabetes_binary" in df.columns:

        st.header("🧾 Dataset Classification Overview")

        st.write(
            "The source dataset contains records assigned "
            "to two classification groups."
        )

        class_values = pd.to_numeric(
            df["Diabetes_binary"],
            errors="coerce",
        ).dropna()

        counts = class_values.value_counts().sort_index()

        labels = {
            0: "Class 0",
            1: "Class 1",
        }

        chart_df = pd.DataFrame({
            "Group": [
                labels.get(value, str(value))
                for value in counts.index
            ],
            "Records": counts.values,
        })

        fig = px.pie(
            chart_df,
            names="Group",
            values="Records",
            title="Distribution of Dataset Groups",
            hole=0.4,
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

        st.caption(
            "These are dataset labels, not personal health categories "
            "or predictions of future diabetes."
        )

    st.divider()

    # =====================================================
    # PRACTICAL HEALTH GUIDANCE
    # =====================================================

    st.header("🌱 Simple Ways to Support Your Health")

    col1, col2 = st.columns(2)

    with col1:

        with st.container(border=True):

            st.subheader("🥗 Balanced Eating")

            st.write(
                "Include vegetables, whole grains, suitable "
                "portions of fruit, and a variety of protein sources."
            )

    with col2:

        with st.container(border=True):

            st.subheader("🚶 Regular Movement")

            st.write(
                "Choose activities that suit your abilities, "
                "such as walking, cycling, or swimming."
            )

    col3, col4 = st.columns(2)

    with col3:

        with st.container(border=True):

            st.subheader("💧 Healthy Habits")

            st.write(
                "Drink water regularly, maintain a consistent "
                "sleep routine, and avoid tobacco."
            )

    with col4:

        with st.container(border=True):

            st.subheader("🩺 Health Screening")

            st.write(
                "Ask a healthcare professional whether diabetes "
                "screening is appropriate for you."
            )

    # =====================================================
    # FINAL NOTE
    # =====================================================

    st.divider()

    st.success(
        "Small, sustainable lifestyle changes can support "
        "your overall well-being."
    )

    st.caption(
        "This application provides educational information, "
        "not medical advice. The model has not been clinically "
        "validated to predict future diabetes onset. Consult "
        "a qualified healthcare professional for screening "
        "and individual medical advice."
    )