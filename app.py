import os
import streamlit as st
from google import genai

st.set_page_config(page_title="AI Elshnawy", page_icon="🤖")

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

st.title("🤖 AI Elshnawy")
st.caption("اسأل أي حاجة — هيبحث في جوجل ويجاوبك فوراً")

# ذاكرة المحادثة (البوت يفتكر اللي فات)
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("اكتب سؤالك هنا...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # بنبعت المحادثة كاملة عشان يفهم السياق
        contents = [m["content"] for m in st.session_state.messages]
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=contents,
            config={"tools": [{"google_search": {}}]},  # Gemini بيدور في جوجل
        )
        st.markdown(response.text)

    st.session_state.messages.append({"role": "assistant", "content": response.text})
