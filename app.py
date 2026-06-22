import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go
from mcq.mcq_generation import MCQGenerator
import time

st.set_page_config(page_title="Interview Prep Pro", page_icon="🚀", layout="centered")

# 🔐 Load secrets
GROQ_API = st.secrets.get("GROQ_API", "")
GOOGLE_API = st.secrets.get("GOOGLE_API", "")

if not GROQ_API:
    st.error("🔑 **GROQ_API key is missing!** If you are on Streamlit Cloud, please add it to your app's Advanced Settings > Secrets.", icon="🛑")
    st.stop()

# 🚀 Initialize MCQ generator
mcq_generator = MCQGenerator(GROQ_API)

# 🎨 Custom CSS for Premium Aesthetics
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Glassmorphism for question card */
    .glass-card {
        background: rgba(22, 27, 34, 0.7);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 30px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        margin-bottom: 24px;
        transition: transform 0.3s ease;
    }
    
    .question-text {
        font-size: 22px;
        font-weight: 600;
        color: #FFFFFF;
        margin-bottom: 20px;
        line-height: 1.5;
    }

    /* Styling radio buttons as clickable modern blocks */
    div[role="radiogroup"] > label {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 15px 20px !important;
        border-radius: 12px;
        margin-bottom: 12px;
        transition: all 0.2s ease-in-out;
        cursor: pointer;
    }
    
    div[role="radiogroup"] > label:hover {
        background: rgba(108, 99, 255, 0.15);
        border-color: #6C63FF;
        transform: translateY(-2px);
    }

    /* Primary Gradient Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #6C63FF 0%, #3B33C3 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: 600;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(108, 99, 255, 0.4);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(108, 99, 255, 0.6);
        color: #fff;
    }

    /* Completion header */
    .completion-header {
        font-size: 32px;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #00C9FF, #92FE9D);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-top: 20px;
        margin-bottom: 30px;
    }
</style>
""", unsafe_allow_html=True)

# 🎯 Sidebar Branding
st.sidebar.markdown(
    """
    <div style="text-align: center; padding-bottom: 20px;">
        <h1 style="font-size: 24px; font-weight: 800; color: #6C63FF;">🚀 Prep Pro</h1>
        <p style="font-size: 14px; color: #8B949E;">Master Your Interview</p>
    </div>
    """, unsafe_allow_html=True
)
st.sidebar.divider()
st.sidebar.markdown("Built with ❤️ by **Team: SHIVAKSH**")
st.sidebar.markdown("🔗 [GitHub Repository](https://github.com/pi-AshuSingh/Interview_Bot)")
st.sidebar.markdown("🔐 **Powered by GROQ**")

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
    with st.spinner("🧠 Synthesizing premium questions..."):
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
        st.warning("Please select an option before submitting.", icon="⚠️")
        return
        
    current_question = st.session_state.questions[index]
    correct_option = next(opt['text'] for opt in current_question['options'] if opt['isCorrect'])
    
    is_correct = (selected_option == correct_option)
    
    st.session_state.user_answers.append({
        'question': current_question['question'],
        'selected_option': selected_option,
        'correct_option': correct_option,
        'is_correct': is_correct
    })
    
    st.session_state.confidence_scores.append(confidence)
    
    if is_correct:
        st.session_state.correct_answers += 1
        st.toast('Spot on! Excellent work.', icon='✅')
    else:
        st.session_state.incorrect_answers += 1
        st.toast('Not quite, but good effort!', icon='💡')
        
    time.sleep(0.5) # Slight delay for UX
    st.session_state.question_index += 1
    st.rerun()

# 💡 Show question
def show_question():
    index = st.session_state.question_index
    total = len(st.session_state.questions)
    current_question = st.session_state.questions[index]
    
    st.progress(index / total)
    st.caption(f"QUESTION {index + 1} OF {total}")
    
    st.markdown(f'''
    <div class="glass-card">
        <div class="question-text">{current_question["question"]}</div>
    </div>
    ''', unsafe_allow_html=True)
    
    options = [opt["text"] for opt in current_question['options']]
    
    st.radio("Select your answer:", options, key=f'selected_option_{index}', label_visibility='collapsed')
    
    st.write("")
    st.slider("Confidence Level (%)", 0, 100, 50, key='confidence')
    st.write("")
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("Submit Answer", use_container_width=True):
            check_answer()

# 🎉 Confetti trigger
def trigger_confetti():
    st.balloons()

# 📊 Summary + Analytics
def display_summary():
    st.markdown('<div class="completion-header">🎉 Assessment Complete!</div>', unsafe_allow_html=True)
    trigger_confetti()
    
    correct = st.session_state.correct_answers
    incorrect = st.session_state.incorrect_answers
    total = correct + incorrect
    score_percentage = round((correct / total) * 100, 1) if total > 0 else 0
    
    # 🎯 Dashboard Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Final Score", f"{score_percentage}%")
    col2.metric("Correct", correct)
    col3.metric("Needs Review", incorrect)
    
    st.divider()
    
    # 📈 Charts Layout
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.markdown("#### Accuracy Breakdown")
        fig = go.Figure(data=[go.Pie(
            labels=['Correct', 'Incorrect'], 
            values=[correct, incorrect], 
            hole=0.6,
            marker_colors=['#00C9FF', '#FF4B2B']
        )])
        fig.update_layout(
            margin=dict(t=20, b=20, l=20, r=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#E6EDF3"
        )
        st.plotly_chart(fig, use_container_width=True)
        
    with chart_col2:
        st.markdown("#### Confidence Progression")
        st.line_chart(st.session_state.confidence_scores, color="#6C63FF")
        
    st.divider()
    st.markdown("### Detailed Review")
    
    for i, ans in enumerate(st.session_state.user_answers):
        with st.expander(f"Q{i+1}: {ans['question'][:60]}..."):
            st.markdown(f"**Question:** {ans['question']}")
            if ans['is_correct']:
                st.success(f"✅ Your answer: {ans['selected_option']}")
            else:
                st.error(f"❌ Your answer: {ans['selected_option']}")
                st.info(f"💡 Correct answer: {ans['correct_option']}")
                
    st.write("")
    btn_col1, btn_col2, btn_col3 = st.columns([1, 1, 1])
    with btn_col1:
        if st.button("🔁 Retake Quiz", use_container_width=True):
            retake()
    with btn_col3:
        if st.button("🏠 Go Home", use_container_width=True):
            reset_state()

# 🧠 Main logic
if not st.session_state.quiz_started:
    st.markdown(
        """
        <div style="text-align: center; padding-top: 40px; padding-bottom: 40px;">
            <h1 style="font-size: 3rem; font-weight: 800; margin-bottom: 0px;">Shivaksh Interview Prep</h1>
            <p style="font-size: 1.2rem; color: #8B949E;">Your AI-powered companion for mastering technical interviews.</p>
        </div>
        """, unsafe_allow_html=True
    )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container(border=True):
            st.session_state.topic = st.selectbox("📚 Choose your Domain", ['Deep Learning', 'Data Science', 'Machine Learning', 'Generative AI', 'Python Development', 'System Design'])
            st.session_state.difficulty_level = st.selectbox("🎯 Difficulty Level", ['Easy', 'Intermediate', 'Advanced', 'Expert'])
            st.session_state.num_questions = st.slider("🔢 Number of questions", 5, 30, 10, step=5)
            st.write("")
            if st.button("🚀 Start Quiz", use_container_width=True):
                start_quiz()
else:
    total = len(st.session_state.questions)
    index = st.session_state.question_index
    
    if index < total:
        show_question()
    else:
        display_summary()
