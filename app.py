import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go
from mcq.mcq_generation import MCQGenerator
import time
from PyPDF2 import PdfReader
import urllib.parse

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
        'show_hint': False,
        'timer_mode': False,
        'question_start_time': 0,
        'session_scores': [],
        'score_saved': False
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
initialize_state()

# 🔁 Reset state
def reset_state():
    for key in ['quiz_started', 'question_index', 'correct_answers', 'incorrect_answers', 'user_answers', 'questions', 'confidence_scores']:
        st.session_state[key] = False if isinstance(st.session_state[key], bool) else [] if isinstance(st.session_state[key], list) else 0
    st.session_state.score_saved = False
    st.rerun()

# 🔄 Retake quiz
def retake():
    st.session_state.quiz_started = True
    st.session_state.question_index = 0
    st.session_state.correct_answers = 0
    st.session_state.incorrect_answers = 0
    st.session_state.user_answers = []
    st.session_state.confidence_scores = []
    st.session_state.question_start_time = time.time()
    st.session_state.score_saved = False
    st.session_state.show_hint = False
    st.rerun()

def extract_pdf_text(pdf_file):
    try:
        reader = PdfReader(pdf_file)
        text = "".join(page.extract_text() for page in reader.pages if page.extract_text())
        return text[:3000] # Limit tokens
    except Exception:
        return ""

# 🧪 Start quiz
def start_quiz(resume_text=""):
    st.session_state.quiz_started = True
    st.session_state.score_saved = False
    
    full_topic = st.session_state.topic
    if st.session_state.sub_topic:
        full_topic += f" ({st.session_state.sub_topic})"
        
    with st.spinner("🧠 Synthesizing premium personalized questions..."):
        questions = mcq_generator.generate(
            topic=full_topic,
            level=st.session_state.difficulty_level,
            number_of_questions=st.session_state.num_questions,
            resume_text=resume_text
        )
        if not questions:
            st.error("❌ Failed to generate questions. Please try again.")
            st.session_state.quiz_started = False
            return
            
        st.session_state.questions = questions
        st.session_state.question_start_time = time.time()
    st.rerun()

# ✅ Check answer
def check_answer():
    index = st.session_state.question_index
    selected_key = f'selected_option_{index}'
    selected_option = st.session_state.get(selected_key)
    confidence = st.session_state.get('confidence', 50)
    
    # Feature 4: Pressure Timer Logic
    time_elapsed = time.time() - st.session_state.question_start_time
    timed_out = False
    if st.session_state.timer_mode and time_elapsed > 30:
        timed_out = True
        st.error(f"⏱️ Time out! You took {int(time_elapsed)} seconds (limit is 30s).")
    elif selected_option is None:
        st.warning("Please select an option before submitting.", icon="⚠️")
        return
        
    current_question = st.session_state.questions[index]
    correct_option = next(opt['text'] for opt in current_question['options'] if opt['isCorrect'])
    
    is_correct = (selected_option == correct_option) and not timed_out
    
    st.session_state.user_answers.append({
        'question': current_question['question'],
        'selected_option': "Time Out" if timed_out else selected_option,
        'correct_option': correct_option,
        'is_correct': is_correct,
        'explanation': current_question.get('explanation', 'No explanation provided.')
    })
    
    st.session_state.confidence_scores.append(confidence)
    
    if is_correct:
        st.session_state.correct_answers += 1
        st.toast('Spot on! Excellent work.', icon='✅')
    elif not timed_out:
        st.session_state.incorrect_answers += 1
        st.toast('Not quite, but good effort!', icon='💡')
    else:
        st.session_state.incorrect_answers += 1
        
    time.sleep(0.8) # Delay for UX
    st.session_state.question_index += 1
    st.session_state.show_hint = False
    st.session_state.question_start_time = time.time()
    st.rerun()

# 💡 Show question
def show_question():
    index = st.session_state.question_index
    total = len(st.session_state.questions)
    current_question = st.session_state.questions[index]
    
    st.progress(index / total)
    
    # Header: Question Num + Timer
    col_a, col_b = st.columns([1, 1])
    with col_a:
        st.caption(f"QUESTION {index + 1} OF {total}")
    with col_b:
        if st.session_state.timer_mode:
            st.caption("⏱️ **Pressure Mode:** 30s limit per question")
    
    # Feature 3: TTS Audio Player via JS
    tts_js = f"""
    <script>
        function speak() {{
            let utterance = new SpeechSynthesisUtterance(`{current_question['question'].replace('`', '')}`);
            speechSynthesis.speak(utterance);
        }}
    </script>
    <button onclick="speak()" style="background:none; border:none; color:#6C63FF; cursor:pointer; font-size:16px;">
        🔊 Read Aloud
    </button>
    """
    
    st.markdown(f'''
    <div class="glass-card">
        {tts_js}
        <div class="question-text">{current_question["question"]}</div>
    </div>
    ''', unsafe_allow_html=True)
    
    options = [opt["text"] for opt in current_question['options']]
    st.radio("Select your answer:", options, key=f'selected_option_{index}', label_visibility='collapsed')
    
    # Feature 2: Hint System
    if st.button("💡 Need a Hint?"):
        st.session_state.show_hint = True
        
    if st.session_state.show_hint:
        st.info(f"**Hint:** {current_question.get('hint', 'Think carefully about the core concepts.')}")
    
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
    
    # Feature 5: Track Session Scores
    if not st.session_state.score_saved:
        st.session_state.session_scores.append({
            "topic": st.session_state.topic, 
            "score": score_percentage, 
            "level": st.session_state.difficulty_level
        })
        st.session_state.score_saved = True
    
    # 🎯 Dashboard Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Final Score", f"{score_percentage}%")
    col2.metric("Correct", correct)
    col3.metric("Needs Review", incorrect)
    
    # Feature 6: Share Score
    tweet_text = urllib.parse.quote(f"I just scored {score_percentage}% on the {st.session_state.difficulty_level} {st.session_state.topic} interview prep bot! 🚀 Try it out: https://shivaksh-interview-prep.streamlit.app/")
    st.markdown(f"[🐦 Share your score on Twitter!](https://twitter.com/intent/tweet?text={tweet_text})")
    
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
        fig.update_layout(margin=dict(t=20, b=20, l=20, r=20), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#E6EDF3")
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
            st.markdown(f"**Explanation:** {ans['explanation']}")
                
    st.write("")
    
    # 📄 Export Report Feature
    report_lines = [f"# Interview Prep Pro - Performance Report\n**Score:** {score_percentage}%\n\n"]
    for i, ans in enumerate(st.session_state.user_answers):
        report_lines.append(f"### Q{i+1}: {ans['question']}")
        report_lines.append(f"- **Your Answer:** {ans['selected_option']} " + ("✅" if ans['is_correct'] else "❌"))
        if not ans['is_correct']:
            report_lines.append(f"- **Correct Answer:** {ans['correct_option']}")
        report_lines.append(f"\n**Explanation:** {ans['explanation']}\n---")
    report_text = "\n".join(report_lines)
    
    btn_col1, btn_col2, btn_col3 = st.columns([1, 1, 1])
    with btn_col1:
        st.download_button(label="📄 Download Report", data=report_text, file_name="Interview_Prep_Report.md", mime="text/markdown", use_container_width=True)
    with btn_col2:
        if st.button("🔁 Retake Quiz", use_container_width=True):
            retake()
    with btn_col3:
        if st.button("🏠 Go Home", use_container_width=True):
            reset_state()

# 🧠 Main logic - Home Page
if not st.session_state.quiz_started:
    st.markdown(
        """
        <div style="text-align: center; padding-top: 20px; padding-bottom: 20px;">
            <h1 style="font-size: 3rem; font-weight: 800; margin-bottom: 0px;">Shivaksh Interview Prep</h1>
            <p style="font-size: 1.2rem; color: #8B949E;">Your AI-powered companion for mastering technical interviews.</p>
        </div>
        """, unsafe_allow_html=True
    )
    
    # Tabs layout for Home Page
    tab_quiz, tab_features, tab_leaderboard, tab_tips = st.tabs(["🚀 Start Quiz", "🌟 Features (New!)", "🏆 Session Leaderboard", "💡 Interview Tips"])
    
    with tab_quiz:
        with st.container(border=True):
            col_t1, col_t2 = st.columns(2)
            with col_t1:
                st.session_state.topic = st.selectbox("📚 Domain", ['Deep Learning', 'Data Science', 'Machine Learning', 'Generative AI', 'Python Development', 'System Design'])
            with col_t2:
                # Feature 7: Sub-topic Drilldown
                st.session_state.sub_topic = st.text_input("🔬 Specific Sub-topic (Optional)", placeholder="e.g. Pandas, Neural Nets")
            
            col_l1, col_l2 = st.columns(2)
            with col_l1:
                st.session_state.difficulty_level = st.selectbox("🎯 Difficulty Level", ['Easy', 'Intermediate', 'Advanced', 'Expert'])
            with col_l2:
                st.session_state.num_questions = st.slider("🔢 Number of questions", 5, 30, 10, step=5)
            
            st.divider()
            # Feature 1: Resume Analyzer
            st.markdown("#### 📄 Personalize with Resume (Optional)")
            st.caption("Upload your resume and Groq will generate questions tailored to your exact skills!")
            resume_file = st.file_uploader("Upload Resume (PDF)", type=['pdf'])
            
            # Feature 4: Timer Toggle
            st.session_state.timer_mode = st.toggle("⏱️ Enable Pressure Timer (30s per question)")
            
            st.write("")
            if st.button("🚀 Start Quiz", use_container_width=True, type="primary"):
                extracted_text = extract_pdf_text(resume_file) if resume_file else ""
                start_quiz(extracted_text)
                
    with tab_features:
        st.markdown("""
        ### 🔥 The Award-Winning 10x Upgrade
        We have added 10 incredible features to revolutionize your prep:
        1. **📄 AI Resume Analyzer**: Upload your PDF resume to get perfectly tailored questions!
        2. **💡 Interactive Hint System**: Get subtle nudges without spoiling the answer.
        3. **🎙️ Text-to-Speech (TTS)**: Click the "Read Aloud" button for audio feedback.
        4. **⏱️ Pressure Timer**: A strict 30-second countdown to simulate real interview stress.
        5. **📈 Session Tracking**: Your scores are logged throughout your current session.
        6. **🔗 Share Score**: Instantly tweet your high scores to your network.
        7. **🎯 Sub-topic Drilldown**: Narrow down broad domains to specific frameworks.
        8. **📚 Interview Tips**: Check the dedicated tips tab for advice.
        9. **🏆 Session Leaderboard**: Compete against yourself with a tracked high-score board.
        10. **🧠 AI Explanations**: Groq generates deep explanations for every correct/incorrect answer.
        """)
        
    with tab_leaderboard:
        if st.session_state.session_scores:
            st.markdown("### 🏆 Your Session High Scores")
            sorted_scores = sorted(st.session_state.session_scores, key=lambda x: x['score'], reverse=True)
            for i, s in enumerate(sorted_scores):
                st.metric(label=f"#{i+1} - {s['topic']} ({s['level']})", value=f"{s['score']}%")
        else:
            st.info("No scores yet. Complete a quiz to see your leaderboard!")
            
    with tab_tips:
        st.markdown("""
        ### 💡 Top Technical Interview Tips
        - **Think Out Loud**: Communication is just as important as the correct answer. Tell the interviewer *how* you are solving the problem.
        - **Clarify Requirements**: Never jump straight into coding or answering without clarifying edge cases first.
        - **Admit When You Don't Know**: It's better to say "I'm not exactly sure, but here is how I would approach finding out..." than to guess wildly.
        - **Review Fundamentals**: For advanced roles, you still need to know the absolute basics perfectly.
        - **Use This App!**: Run the *Pressure Timer Mode* to get used to thinking under stress.
        """)
else:
    total = len(st.session_state.questions)
    index = st.session_state.question_index
    
    if index < total:
        show_question()
    else:
        display_summary()
