# Interview-Preparation-Stremlit-App

This bot will prepare you for interview by generating MCQs and provide feedback.

## How to Use
1. Clone the repo: `git clone https://github.com/Muhammad-Shah/Interview-Preparation-Stremlit-App.git`
2. Install dependencies `pip install -r requirements.txt`
3. create `.env` file in the root of the folder and put `GROQ_API = 'Your API KEY'`
4. Open `app.py` at the top uncomment 
`from dotenv import load_dotenv
import os
dotenv_path = 'env'
load_dotenv(dotenv_path)
GROQ_API = os.getenv('GROQ_API')
`
comment
`GROQ_API = st.secrets["GROQ_API"]`
5. Run command: `streamlit run app.py`

## Demo

![initial screen](demo/1.png)

![question screen 1](demo/2.png)

![question screen 2](demo/3.png)

![question screen 3](demo/4.png)

![question screen 4](demo/5.png)

![question screen 5](demo/6.png)
