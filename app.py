import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go
from mcq.mcq_generation import MCQGenerator

# 🔐 Load secrets
GROQ_API = st.secrets["GROQ_API"]
GOOGLE_API = st.secrets["GOOGLE_API"]

# 🚀 Initialize MCQ generator
mcq_generator = MCQGenerator(GOOGLE_API)

# 🎨 Custom CSS
st.markdown("""
<style>
.question-text {
    font-size: 20px;
    font-weight: 600;
    padding: 12px;
    margin-bottom: 12px;
    background-color: #433D8B;
    color: white;
    border-radius: 8px;
}
.stRadio label {
    background-color: #E0E0F8;
    padding: 10px;
    border-radius: 8px;
    margin-bottom: 8px;
    font-size: 16px;
}
.completion-message {
    font-size: 24px;
    font-weight: bold;
    color: #4CAF50;
    text-align: center;
    margin-top: 30px;
}
</style>
""", unsafe_allow_html=True)

# 🎯 Sidebar Branding
st.sidebar.title("🚀 Interview Prep Pro")
st.sidebar.markdown("Built with ❤️ by **Team: SHIVAKSH**")
st.sidebar.markdown("[GitHub Repo](https://github.com/pi-AshuSingh/Interview_Bot)")
st.sidebar.markdown("🔐 Powered by GROQ + Google APIs")

# 🧠 Initialize session state
def initialize_state():
    defaults = {
        'quiz_started': False,
        'question_index': 0,
        'correct_answers': 0,
        'incorrect_answers': 0,
        'user_answers': [],
        'questions': [],
        'confidence_scores': [],
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
initialize_state()

# 🔁 Reset state
def reset_state():
    for key in ['quiz_started', 'question_index', 'correct_answers', 'incorrect_answers', 'user_answers', 'questions', 'confidence_scores']:
        st.session_state[key] = False if isinstance(st.session_state[key], bool) else [] if isinstance(st.session_state[key], list) else 0
    st.rerun()

# 🔄 Retake quiz
def retake():
    st.session_state.quiz_started = True
    st.session_state.question_index = 0
    st.session_state.correct_answers = 0
    st.session_state.incorrect_answers = 0
    st.session_state.user_answers = []
    st.session_state.confidence_scores = []
    st.rerun()

# 🧪 Start quiz
def start_quiz():
    st.session_state.quiz_started = True
    with st.spinner("🧠 Generating questions..."):
        questions = mcq_generator.generate(
            topic=st.session_state.topic,
            level=st.session_state.difficulty_level,
            number_of_questions=st.session_state.num_questions,
        )
        if not questions:
            st.error("❌ Failed to generate questions. Please try again.")
            st.session_state.quiz_started = False
            return
        st.session_state.questions = questions
    st.rerun()

# ✅ Check answer
def check_answer():
    index = st.session_state.question_index
    selected_key = f'selected_option_{index}'
    selected_option = st.session_state.get(selected_key)
    confidence = st.session_state.get('confidence', 50)
    if selected_option is None:
        st.warning("Please select an option before submitting.")
        return
    current_question = st.session_state.questions[index]
    correct_option = next(opt['text'] for opt in current_question['options'] if opt['isCorrect'])
    st.session_state.user_answers.append({
        'question': current_question['question'],
        'selected_option': selected_option,
        'correct_option': correct_option
    })
    st.session_state.confidence_scores.append(confidence)
    if selected_option == correct_option:
        st.session_state.correct_answers += 1
    else:
        st.session_state.incorrect_answers += 1
    st.session_state.question_index += 1
    st.rerun()

# 💡 Show question
def show_question():
    index = st.session_state.question_index
    current_question = st.session_state.questions[index]
    st.markdown(f'<div class="question-text">{current_question["question"]}</div>', unsafe_allow_html=True)
    options = [opt["text"] for opt in current_question['options']]
    st.radio("Choose an option:", options, key=f'selected_option_{index}', label_visibility='hidden')
    st.slider("How confident are you?", 0, 100, 50, key='confidence')
    if st.button("Submit"):
        check_answer()

# 🎉 Confetti trigger
def trigger_confetti():
    components.html("<script>confetti();</script>", height=0)

# 📊 Summary + Analytics
def display_summary():
    st.markdown('<div class="completion-message">🎉 Quiz Completed!</div>', unsafe_allow_html=True)
    trigger_confetti()
    correct = st.session_state.correct_answers
    incorrect = st.session_state.incorrect_answers
    total = correct + incorrect
    score = round((correct / total) * 10, 2) if total > 0 else 0
    st.markdown(f"🏆 Final Score: **{score}/10**")
    st.markdown(f"✅ Correct: **{correct}**")
    st.markdown(f"❌ Incorrect: **{incorrect}**")
    fig = go.Figure(data=[go.Pie(labels=['Correct', 'Incorrect'], values=[correct, incorrect], hole=0.4)])
    st.plotly_chart(fig)
    st.markdown("📈 Confidence per question:")
    st.line_chart(st.session_state.confidence_scores)
    for ans in st.session_state.user_answers:
        st.write(f"**Q:** {ans['question']}")
        if ans['selected_option'] == ans['correct_option']:
            st.success(f"✅ Your answer: {ans['selected_option']}")
        else:
            st.error(f"❌ Your answer: {ans['selected_option']}")
            st.info(f"✅ Correct answer: {ans['correct_option']}")
        st.write("---")
    if st.button("🔁 Retake Quiz"):
        retake()
    if st.button("🏠 Home"):
        reset_state()

# 🧠 Main logic
if not st.session_state.quiz_started:
    st.title("🧠 Interview Preparation App")
    st.session_state.topic = st.selectbox("📚 Select a topic", ['Deep Learning', 'Data Science', 'Machine Learning', 'Generative AI'])
    st.session_state.difficulty_level = st.selectbox("🎯 Difficulty", ['Easy', 'Intermediate', 'Advanced'])
    st.session_state.num_questions = st.slider("🔢 Number of questions", 5, 30, 10, step=5)
    if st.button("🚀 Start Quiz"):
        start_quiz()
else:
    total = len(st.session_state.questions)
    index = st.session_state.question_index
    st.progress(index / total if total > 0 else 0)
    st.write(f"📖 Question {index + 1} of {total}")
    if index < total:
        show_question()
    else:
        display_summary()
