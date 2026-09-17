import streamlit as st
from groq import Groq

# ---- 1. Page setup ----
st.set_page_config(page_title="AI Vocabulary Assistant", page_icon="📚")
st.title("📚 AI Vocabulary Assistant")
st.write("Enter a word or question, and get a simple explanation back.")

# ---- Privacy notice (Part 12) ----
st.info(
    "⚠️ AI responses can contain mistakes — please verify important information. "
    "Do not enter passwords, addresses, ID numbers, or other private information."
)

# ---- 2. Connect to the LLM using your API key ----
# Store your key in Streamlit Secrets as:
# GROQ_API_KEY = "your-key-here"
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except KeyError:
    st.error("API key not found. Please set GROQ_API_KEY in your Streamlit Secrets.")
    st.stop()

# ---- 3. User-controlled options (Part 10) ----
col1, col2 = st.columns(2)
with col1:
    style = st.selectbox("Explanation style:", ["Simple", "Detailed"])
with col2:
    length = st.selectbox("Answer length:", ["Short", "Long"])

# ---- 4. Text input box ----
user_question = st.text_input("Type a word or question here:")

# ---- 5. Button to send the message ----
if st.button("Ask"):
    if user_question.strip() == "":
        st.warning("Please type something first.")
    else:
        # Build the system instruction based on the user's chosen options
        system_instruction = (
            f"You are a friendly vocabulary assistant. "
            f"Explain words or answer questions in {style.lower()} English, "
            f"easy to understand. Keep your answer {length.lower()}."
        )

        # ---- 6. Send the message to the LLM, with error handling (Part 11) ----
        try:
            with st.spinner("Thinking..."):
                response = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    max_tokens=500,
                    timeout=20,
                    messages=[
                        {"role": "system", "content": system_instruction},
                        {"role": "user", "content": user_question}
                    ],
                )
                answer = response.choices[0].message.content

            # ---- 7. Display the LLM's response ----
            st.subheader("Answer:")
            st.write(answer)

        except Exception as e:
            error_text = str(e).lower()
            if "rate" in error_text or "quota" in error_text or "429" in error_text:
                st.error("The free usage limit has been reached. Please try again later.")
            elif "auth" in error_text or "api key" in error_text or "401" in error_text:
                st.error("There was a problem with the API key. Please check it is set correctly.")
            elif "timeout" in error_text:
                st.error("The request took too long and timed out. Please try again.")
            elif "not found" in error_text or "404" in error_text:
                st.error("The selected model is unavailable right now.")
            else:
                st.error("Something went wrong while contacting the AI. Please try again.")
