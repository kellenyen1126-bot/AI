import streamlit as st
from groq import Groq

# ---- 1. Page setup ----
st.set_page_config(page_title="AI Vocabulary Assistant", page_icon="📚")
st.title("📚 AI Vocabulary Assistant")
st.write("Enter a word or question, and get a simple explanation back.")

# ---- 2. Connect to the LLM using your API key ----
# Store your key in .streamlit/secrets.toml as:
# GROQ_API_KEY = "your-key-here"
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ---- 3. Text input box ----
user_question = st.text_input("Type a word or question here:")

# ---- 4. Button to send the message ----
if st.button("Ask"):
    if user_question.strip() == "":
        st.warning("Please type something first.")
    else:
        # ---- 5. Send the message to the LLM ----
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                max_tokens=500,
                messages=[
                    {"role": "system", "content": "You are a friendly vocabulary assistant. Explain words or answer questions in simple, easy-to-understand English."},
                    {"role": "user", "content": user_question}
                ],
            )
            answer = response.choices[0].message.content

        # ---- 6. Display the LLM's response ----
        st.subheader("Answer:")
        st.write(answer)
