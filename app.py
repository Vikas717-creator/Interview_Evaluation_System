import streamlit as st
import pandas as pd
import plotly.express as px
from question_loader import load_questions
from evaluator import AnswerEvaluator
from datetime import datetime
import voice_input

st.set_page_config(page_title="AI Interview System", layout="wide")

st.title("🤖 AI Powered Interview Evaluation System")


# -----------------------------
# SESSION STATE
# -----------------------------

if "started" not in st.session_state:
    st.session_state.started = False

if "questions" not in st.session_state:
    st.session_state.questions = []

if "question_index" not in st.session_state:
    st.session_state.question_index = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "evaluator" not in st.session_state:
    st.session_state.evaluator = None

if "result_saved" not in st.session_state:
    st.session_state.result_saved = False

if "answer_submitted" not in st.session_state:
    st.session_state.answer_submitted = False

if "last_label" not in st.session_state:
    st.session_state.last_label = None
    
if "voice_text" not in st.session_state:
    st.session_state.voice_text = ""

if "name" not in st.session_state:
    st.session_state.name = ""

if "branch" not in st.session_state:
    st.session_state.branch = ""

if "course" not in st.session_state:
    st.session_state.course = ""

if "subject" not in st.session_state:
    st.session_state.subject = ""

# -----------------------------
# SIDEBAR
# -----------------------------

st.sidebar.title("Navigation")

menu = st.sidebar.radio(
    "Go To",
    ["Home", "Dashboard"]
)

if st.session_state.name:
    st.sidebar.markdown("---")
    st.sidebar.write("👤 User:", st.session_state.name)
    st.sidebar.write("📚 Subject:", st.session_state.subject)
    st.sidebar.write("🏆 Score:", st.session_state.score)
if st.session_state.name == "":
    st.sidebar.info("Start an interview to see stats")


# -----------------------------
# HOME PAGE
# -----------------------------

if menu == "Home":

    # -------- DETAILS SCREEN --------
    if not st.session_state.started:

        st.subheader("Enter Your Details")

        name = st.text_input("Name")
        branch = st.text_input("Branch")
        course = st.text_input("Course")

        subject = st.selectbox(
            "Select Interview Subject",
            ["Python", "Java", "Data Science"]
        )

        if st.button("Start Interview"):

            if name.strip() == "":
                st.warning("Please enter your name")
                st.stop()

            st.session_state.started = True
            st.session_state.name = name
            st.session_state.branch = branch
            st.session_state.course = course
            st.session_state.subject = subject
            
            if subject == "Python":
                file = "python_questions.json"
            elif subject == "Java":
                file = "java_questions.json"
            else:
                file = "datascience_questions.json"

            st.session_state.questions = load_questions(file)
            
            st.session_state.evaluator = AnswerEvaluator()

            st.session_state.question_index = 0
            st.session_state.score = 0
            st.session_state.result_saved = False

            st.rerun()

    # -------- INTERVIEW QUESTIONS --------
    elif st.session_state.question_index < len(st.session_state.questions):
        
        questions = st.session_state.questions
        index = st.session_state.question_index
        total = len(questions)

        q = questions[index]

        st.subheader(f"Question {index + 1}")
        st.progress((index + 1) / total)
        st.info(f"Question {index + 1} of {total}")

        st.write(q["question"])

        # ---------------- ANSWER INPUT ----------------

        if not st.session_state.answer_submitted:

            col1, col2 = st.columns([3, 1])

            with col1:
                user_answer = st.text_area(
                    "Your Answer",
                    value=st.session_state.voice_text,
                    key=f"answer_{index}"
                )

            with col2:

                if st.button("🎤 Speak Answer"):

                    st.info("Listening...")

                    text = voice_input.speech_to_text()

                    if text:
                        st.session_state.voice_text = text
                        st.rerun()

                    else:
                        st.warning("Could not understand audio")

            if st.button("Submit Answer"):

                user_answer = st.session_state.get(
                    f"answer_{index}", ""
                )

                if user_answer.strip() == "":
                    st.warning("Please enter your answer")
                    st.stop()

                evaluator = st.session_state.evaluator

                ref = evaluator.encode_references(q["answers"])

                score = evaluator.evaluate(user_answer, ref)

                label = evaluator.get_label(score)

                numeric = evaluator.get_numeric_score(score)

                st.session_state.score += numeric
                st.session_state.last_label = label
                st.session_state.answer_submitted = True
                st.session_state.voice_text = ""

                st.rerun()

        # ---------------- SHOW RESULT ----------------

        else:

            if st.session_state.last_label == "Correct":
                st.success("Correct Answer")

            elif st.session_state.last_label == "Partially Correct":
                st.warning("Partially Correct")

            else:
                st.error("Wrong Answer")

            if st.button("Next Question"):

                st.session_state.question_index += 1
                st.session_state.answer_submitted = False
                st.session_state.last_label = None
                st.session_state.voice_text = ""

                st.rerun()

    # -------- RESULT SCREEN --------

    else:

        final_score = st.session_state.score

        st.success(
            f"Interview Completed! Final Score: {final_score}/10"
        )

        if not st.session_state.result_saved:

            data = {
                "name": st.session_state.name,
                "branch": st.session_state.branch,
                "course": st.session_state.course,
                "subject": st.session_state.subject,
                "score": final_score,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M")
            }

            df = pd.DataFrame([data])

            try:
                old = pd.read_csv("results.csv")
                df = pd.concat([old, df])
            except:
                pass

            df.to_csv("results.csv", index=False)

            st.session_state.result_saved = True

        if st.button("Restart Interview"):

            st.session_state.started = False
            st.session_state.questions = []
            st.session_state.question_index = 0
            st.session_state.score = 0
            st.session_state.result_saved = False

            st.rerun()

# -----------------------------
# DASHBOARD
# -----------------------------

elif menu == "Dashboard":

    st.header("📊 Performance Dashboard")

    try:
        df = pd.read_csv("results.csv")
    except:
        st.warning("No attempts yet.")
        st.stop()
    if "subject" not in df.columns:
        df["subject"] = "Python"

    if df.empty:
        st.warning("No attempts yet.")
        st.stop()

    df["attempt"] = range(1, len(df) + 1)
    
    if st.session_state.name != "":
        user_df = df[df["name"] == st.session_state.name]
    else:
        user_df = df
        
    user_df = user_df.reset_index(drop=True)
    user_df["attempt"] = range(1, len(user_df) + 1)


    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Attempts", len(user_df))
    col2.metric("Average Score", round(user_df["score"].mean(), 2))
    col3.metric("Best Score", user_df["score"].max())
    col4.metric("Lowest Score", user_df["score"].min())

    st.divider()

    st.subheader("📈 Score Trend")

    fig = px.line(
        user_df,
        x="attempt",
        y="score",
        color="subject",
        title="Your Score Trends",
        markers=True
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Score Distribution")

    col1, col2 = st.columns(2)

    with col1:
        fig1 = px.histogram(user_df, x="score", nbins=10, title="Your Score Distribution")
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        fig2 = px.bar(user_df, x="subject", y="score",color="subject", title="Scores by Subject")
        st.plotly_chart(fig2, use_container_width=True)
        
    st.subheader("Subject-wise Performance")
    fig3 = px.bar(
        user_df,
        x="subject",
        y="score",
        color="subject",
        title="Your Performance by Subject"
    )

    st.plotly_chart(fig3, use_container_width=True)

    st.subheader("Attempt History")

    st.dataframe(
        user_df.drop(columns=["attempt"]).sort_values(
            "score", ascending=False
        ),
        use_container_width=True
    )
# -----------------------------
# SAVE RESULT AFTER INTERVIEW
# -----------------------------

if (
    st.session_state.started
    and st.session_state.question_index >= len(st.session_state.questions)
    and not st.session_state.result_saved
):

    final_score = st.session_state.score

    st.success(f"Interview Completed! Final Score: {final_score}/10")

    data = {
        "name": st.session_state.name,
        "branch": st.session_state.branch,
        "course": st.session_state.course,
        "score": final_score,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    df = pd.DataFrame([data])

    try:
        old = pd.read_csv("results.csv")
        df = pd.concat([old, df])
    except:
        pass

    df.to_csv("results.csv", index=False)

    st.session_state.result_saved = True

    if st.button("Restart Interview"):

        st.session_state.started = False
        st.session_state.questions = []
        st.session_state.question_index = 0
        st.session_state.score = 0
        st.session_state.result_saved = False

        st.rerun()