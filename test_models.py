import google.generativeai as genai
import toml

secrets = toml.load('/Users/ashutoshkumarsingh/Downloads/Interview_Bot/.streamlit/secrets.toml')
genai.configure(api_key=secrets['GOOGLE_API'])

try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)
except Exception as e:
    print(e)
