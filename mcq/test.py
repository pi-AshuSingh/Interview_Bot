import streamlit as st
from mcq.mcq_generation import mcq_generation

# Inject custom CSS for better styling
st.markdown(
    """
    <style>
    .question-text {
        font-size: 18px;
        font-weight: bold;
        padding: 10px;
        margin-bottom: 10px;
        background-color: #4C3BCF;
        border-radius: 5px;
    }
    .answer-text {
        font-size: 16px;
        padding: 8px;
        margin-bottom: 5px;
        border-radius: 5px;
    }
    .correct-answer {
        background-color: #d4edda;
        color: #155724;
    }
    .incorrect-answer {
        background-color: #f8d7da;
        color: #721c24;
    }
    .summary {
        border-top: 1px solid #e0e0e0;
        padding-top: 10px;
        margin-top: 20px;
    }
    .completion-message {
        font-size: 20px;
        font-weight: bold;
        color: #4CAF50;
        margin-bottom: 20px;
    }
    .stats {
        font-size: 18px;
        margin-bottom: 20px;
    }
    .summary-header {
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    /* Custom CSS for radio buttons */
    .stRadio > div {
        padding: 10px;
        font-size: 18px;
    }
    .stRadio div[role='radiogroup'] {
        display: flex;
        flex-direction: column;
    }
    .stRadio label {
        background-color: #071952; /* Change this to your desired color */
        padding: 0.5rem;
        border-radius: 0.5rem;
        margin-bottom: 0.5rem;
        width: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize session state variables
if 'quiz_started' not in st.session_state:
    st.session_state.quiz_started = False
if 'question_index' not in st.session_state:
    st.session_state.question_index = 0
if 'correct_answers' not in st.session_state:
    st.session_state.correct_answers = 0
if 'incorrect_answers' not in st.session_state:
    st.session_state.incorrect_answers = 0
if 'user_answers' not in st.session_state:
    st.session_state.user_answers = []
if 'questions' not in st.session_state:
    st.session_state.questions = []

# Function to start quiz


def start_quiz():
    st.session_state.quiz_started = True
    st.session_state.question_index = 0
    st.session_state.correct_answers = 0
    st.session_state.incorrect_answers = 0
    st.session_state.user_answers = []
    st.session_state.questions = mcq_generation(
        topic=st.session_state.topic,
        defficulty_level=st.session_state.difficulty_level
    )
    st.experimental_rerun()

# Function to reset quiz state


def reset_quiz():
    st.session_state.quiz_started = False
    st.session_state.question_index = 0
    st.session_state.correct_answers = 0
    st.session_state.incorrect_answers = 0
    st.session_state.user_answers = []
    st.experimental_rerun()


# Display topic and difficulty level selection if quiz has not started
if not st.session_state.quiz_started:
    st.title("Interview Preparation Application")

    st.session_state.topic = st.selectbox(
        "Select a topic to prepare for interview",
        options=['Deep Learning', 'Data Science',
                 'Machine Learning', 'Generative AI']
    )
    st.session_state.difficulty_level = st.selectbox(
        "Select your difficulty level",
        options=['Easy', 'Intermediate', 'Advanced']
    )

    # Display instructions
    st.header("Instructions")
    st.markdown(
        "Select an option to begin the quiz. After selecting an option, questions will be displayed one by one.")

    # Display start quiz button
    if st.button("Start Quiz"):
        start_quiz()

# Display the progress bar and question index
if st.session_state.quiz_started:
    total_questions = len(st.session_state.questions)
    progress = (st.session_state.question_index) / total_questions
    st.progress(progress)
    st.write(
        f"Question {st.session_state.question_index + 1} of {total_questions}")

# Function to check the user's answer and update the state


def check_answer():
    selected_option = st.session_state.selected_option
    current_question = st.session_state.questions[st.session_state.question_index]

    # Track the question, selected option, and the correct option
    correct_option = next(
        option['text'] for option in current_question['options'] if option['isCorrect'])
    st.session_state.user_answers.append({
        'question': current_question['question'],
        'selected_option': selected_option,
        'correct_option': correct_option
    })

    if correct_option == selected_option:
        st.session_state.correct_answers += 1
    else:
        st.session_state.incorrect_answers += 1

    # Move to the next question
    st.session_state.question_index += 1
    # Rerun the app to display the next question
    st.experimental_rerun()

# Display the current question


def show_next_question():
    if st.session_state.question_index < len(st.session_state.questions):
        current_question = st.session_state.questions[st.session_state.question_index]

        st.markdown(
            f'<div class="question-text">{current_question["question"]}</div>', unsafe_allow_html=True)

        options = [option['text'] for option in current_question['options']]
        st.radio("Choose an option:", options,
                 key='selected_option', label_visibility='hidden')

        if st.button("Submit"):
            check_answer()

    else:
        st.markdown(
            '<div class="completion-message">Quiz completed!</div>', unsafe_allow_html=True)
        stats_col1, stats_col2 = st.columns(2)
        with stats_col1:
            st.markdown('<div class="stat-box"><div class="stat-header">Correct Answers</div><div class="stat-value">{}</div></div>'.format(
                st.session_state.correct_answers), unsafe_allow_html=True)
        with stats_col2:
            st.markdown('<div class="stat-box"><div class="stat-header">Incorrect Answers</div><div class="stat-value">{}</div></div>'.format(
                st.session_state.incorrect_answers), unsafe_allow_html=True)

        # Display the summary of all questions and answers
        st.markdown(
            '<div class="summary-header">Summary of your answers:</div>', unsafe_allow_html=True)
        for answer in st.session_state.user_answers:
            st.write(f"**Question:** {answer['question']}")
            if answer['selected_option'] == answer['correct_option']:
                st.success(f"**Your answer:** {answer['selected_option']}")
            else:
                st.success(f"**Correct answer:** {answer['correct_option']}")
                st.error(f"**Your answer:** {answer['selected_option']}")
            st.write("---")

        # Add buttons for retaking the quiz and going to the home screen
        if st.button("Retake Quiz"):
            start_quiz()
        if st.button("Go to Home Screen"):
            reset_quiz()


# Display questions if quiz has started
if st.session_state.quiz_started:
    show_next_question()
else:
    st.header("Multiple Choice Questions")
