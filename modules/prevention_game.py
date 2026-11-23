import streamlit as st


def prevention_game_page():

    st.title("🎮 Diabetes Prevention Quest")

    st.write(
        "Build healthier habits through simple questions, "
        "daily challenges, and interactive learning."
    )

    st.info(
        "Your points measure game progress, not your medical "
        "risk or a reduction in diabetes risk."
    )

    # --------------------------------------------------
    # INITIALIZE GAME STATE
    # --------------------------------------------------

    if "quest_points" not in st.session_state:
        st.session_state.quest_points = 0

    if "quest_completed" not in st.session_state:
        st.session_state.quest_completed = []

    if "quest_answers" not in st.session_state:
        st.session_state.quest_answers = {}

    if "quest_challenge_done" not in st.session_state:
        st.session_state.quest_challenge_done = []

    # --------------------------------------------------
    # QUESTIONS
    # --------------------------------------------------

    questions = [
        {
            "question": (
                "1. You want to improve your health. "
                "What is a good first step?"
            ),
            "options": [
                "Make one small, realistic change",
                "Change every habit overnight",
                "Wait until you become unwell",
            ],
            "answer": "Make one small, realistic change",
            "explanation": (
                "Small, achievable changes are often easier "
                "to maintain over time."
            ),
        },
        {
            "question": (
                "2. Which is a sensible everyday drink choice "
                "for many people?"
            ),
            "options": [
                "Water instead of a sugary drink",
                "Sugary drinks throughout the day",
                "Avoid drinking water all day",
            ],
            "answer": "Water instead of a sugary drink",
            "explanation": (
                "Choosing water instead of sugary drinks can "
                "help reduce added sugar intake."
            ),
        },
        {
            "question": (
                "3. What can help support general health?"
            ),
            "options": [
                "Regular physical activity suited to you",
                "Sitting all day whenever possible",
                "Sleeping as little as possible",
            ],
            "answer": "Regular physical activity suited to you",
            "explanation": (
                "Regular physical activity supports general "
                "health. Choose an activity appropriate for "
                "your abilities and health."
            ),
        },
        {
            "question": (
                "4. If your health assessment concerns you, "
                "what should you do?"
            ),
            "options": [
                "Ignore it completely",
                "Discuss appropriate screening with a healthcare professional",
                "Treat the app result as a diagnosis",
            ],
            "answer": (
                "Discuss appropriate screening with a healthcare professional"
            ),
            "explanation": (
                "A healthcare professional can assess your "
                "circumstances and advise whether testing is needed."
            ),
        },
        {
            "question": (
                "5. Which is a useful approach to meals?"
            ),
            "options": [
                "Eat balanced meals with suitable portions",
                "Skip every meal",
                "Eat only sugary foods",
            ],
            "answer": "Eat balanced meals with suitable portions",
            "explanation": (
                "Balanced meals can include vegetables, "
                "whole grains, and suitable portions of "
                "protein-rich foods."
            ),
        },
    ]

    # --------------------------------------------------
    # PROGRESS SUMMARY
    # --------------------------------------------------

    total_questions = len(questions)
    completed_count = len(st.session_state.quest_completed)

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "⭐ Quest Points",
        st.session_state.quest_points,
    )

    c2.metric(
        "✅ Questions Completed",
        f"{completed_count}/{total_questions}",
    )

    c3.metric(
        "🏆 Challenges Completed",
        len(st.session_state.quest_challenge_done),
    )

    progress = completed_count / total_questions

    st.progress(progress)

    st.caption(
        f"Quiz progress: {completed_count}/{total_questions} questions"
    )

    st.divider()

    # --------------------------------------------------
    # INTERACTIVE QUIZ
    # --------------------------------------------------

    st.header("🧠 Health Knowledge Challenge")

    for index, question in enumerate(questions):

        question_key = f"quest_question_{index}"

        with st.container(border=True):

            st.subheader(question["question"])

            if index in st.session_state.quest_completed:

                selected = st.session_state.quest_answers[index]

                if selected == question["answer"]:

                    st.success("Correct answer!")

                else:

                    st.info(
                        f"Your answer: {selected}"
                    )

                    st.write(
                        f"Suggested answer: {question['answer']}"
                    )

                st.write(
                    f"💡 Why? {question['explanation']}"
                )

            else:

                with st.form(key=f"quest_form_{index}"):

                    selected = st.radio(
                        "Choose your answer:",
                        question["options"],
                        key=question_key,
                    )

                    submitted = st.form_submit_button(
                        "Check Answer",
                        use_container_width=True,
                    )

                    if submitted:

                        st.session_state.quest_answers[index] = selected

                        st.session_state.quest_completed.append(index)

                        # Award points for participation.
                        st.session_state.quest_points += 5

                        st.rerun()

    # --------------------------------------------------
    # DAILY WELLNESS CHALLENGES
    # --------------------------------------------------

    st.divider()

    st.header("🌱 Daily Wellness Challenges")

    st.write(
        "Choose realistic activities that fit your health "
        "and daily routine."
    )

    challenges = [
        (
            "🚶 Move your body",
            "Try a short walk or another suitable physical activity.",
        ),
        (
            "🥗 Build a balanced plate",
            "Include vegetables and suitable portions of nutritious foods.",
        ),
        (
            "💧 Choose water",
            "Choose water instead of a sugary drink when appropriate.",
        ),
        (
            "😴 Support your sleep",
            "Plan a consistent bedtime that allows enough rest.",
        ),
        (
            "🩺 Plan a health check",
            "Consider asking a healthcare professional whether screening is appropriate.",
        ),
    ]

    for index, (title, description) in enumerate(challenges):

        with st.container(border=True):

            col1, col2 = st.columns([4, 1])

            with col1:

                st.subheader(title)
                st.write(description)

            with col2:

                if index in st.session_state.quest_challenge_done:

                    st.success("Completed")

                else:

                    if st.button(
                        "Complete",
                        key=f"quest_challenge_{index}",
                        use_container_width=True,
                    ):

                        st.session_state.quest_challenge_done.append(index)

                        st.session_state.quest_points += 10

                        st.rerun()

    # --------------------------------------------------
    # ACHIEVEMENTS
    # --------------------------------------------------

    st.divider()

    st.header("🏆 Your Achievements")

    points = st.session_state.quest_points

    if points >= 50:

        st.success(
            "Habit Hero! You have earned 50 or more quest points."
        )

    elif points >= 25:

        st.success(
            "Healthy Habits Explorer! Keep learning and practising."
        )

    elif points >= 10:

        st.info(
            "Good start! Continue with small, realistic steps."
        )

    else:

        st.write(
            "Complete questions and challenges to earn your first badge."
        )

    st.metric(
        "Total Quest Points",
        points,
    )

    # --------------------------------------------------
    # NEXT STEP
    # --------------------------------------------------

    st.divider()

    st.header("💡 Your Next Step")

    st.write(
        "Choose one healthy habit you can realistically practise today. "
        "Consistency is more important than completing everything at once."
    )

    st.warning(
        "Completing this game does not automatically lower your "
        "diabetes risk or change your model score. The game is for "
        "education and motivation, not diagnosis or treatment."
    )

    # --------------------------------------------------
    # RESET GAME
    # --------------------------------------------------

    with st.expander("Reset game progress"):

        st.write(
            "This clears your current quiz answers, points, "
            "and completed challenges."
        )

        if st.button(
            "Reset My Quest",
            type="secondary",
        ):

            st.session_state.quest_points = 0
            st.session_state.quest_completed = []
            st.session_state.quest_answers = {}
            st.session_state.quest_challenge_done = []

            st.rerun()