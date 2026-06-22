# 🚀 Interview Prep Pro

An AI-powered interview preparation bot that generates customized Multiple Choice Questions (MCQs) for various tech domains, built with Streamlit, Groq, and Langchain.

## 🌟 Features
- **Dynamic Content Generation:** Uses Groq's lightning-fast LLMs to generate high-quality questions on the fly.
- **Customizable Difficulty:** Choose between Easy, Intermediate, Advanced, and Expert.
- **Interactive Quizzes:** Real-time feedback, confidence tracking, and premium UI aesthetics.
- **Detailed Analytics:** Visual breakdown of your performance with Plotly charts.

## 🛠️ Local Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/pi-AshuSingh/Interview_Bot.git
   cd Interview_Bot
   ```
2. Set up the virtual environment and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Add your API key:
   - Create a folder named `.streamlit` and add a file `secrets.toml`
   - Add `GROQ_API="gsk_your_api_key_here"`
4. Run the app:
   ```bash
   streamlit run app.py
   ```

## 🚀 Deployment to Streamlit Community Cloud

The easiest way to deploy this application for free is using Streamlit Community Cloud:

1. Ensure your code is pushed to your GitHub repository.
2. Sign in to [Streamlit Community Cloud](https://share.streamlit.io/) with your GitHub account.
3. Click **New app** and grant Streamlit access to your repositories.
4. Select the repository `pi-AshuSingh/Interview_Bot`, branch `main`, and the main file path `app.py`.
5. Click on **Advanced settings** before hitting deploy!
6. In the **Secrets** section, paste your environment variables in TOML format:
   ```toml
   GROQ_API="gsk_your_actual_api_key_here"
   ```
7. Click **Deploy!** Your app will be live on the web in a few minutes.

---
Built with ❤️ by **Team: SHIVAKSH**
