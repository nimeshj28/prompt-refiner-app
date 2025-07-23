import streamlit as st
import os

# Optional: For later use when you get the key
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

# --- Check for OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY", None)

if openai_api_key:
    import openai
    openai.api_key = openai_api_key
else:
    st.warning("Running in Demo Mode — no API key found.")

# --- UI
st.set_page_config(page_title="Prompt Refiner", layout="centered")
st.title("🎯 AI Prompt Refiner (Demo Mode Available)")

st.write("Enter a **Role**, some **Context**, and a **Task** — get a cleaner prompt!")

# Inputs
role = st.text_input("🧑 Role (What should the AI act as?)")
context = st.text_area("📄 Context (Background info)")
task = st.text_area("✅ Task (What do you want the AI to do?)")

# Button
if st.button("🔍 Refine Prompt"):
    if not role or not task:
        st.error("Please fill Role and Task at least.")
    else:
        with st.spinner("Refining your prompt..."):
            if openai_api_key:
                # Actual GPT call (when key is present)
                system_prompt = """
                You are a Prompt Engineer. Given a Role, Context, and Task:
                - Create a clean and concise prompt
                - Define the expected response format
                - List assumptions made
                """
                user_message = f"Role: {role}\nContext: {context}\nTask: {task}"
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_message}
                    ],
                    temperature=0.7
                )
                result = response["choices"][0]["message"]["content"]
            else:
                # Mock response for demo
                result = f"""
**Refined Prompt**:  
You are a {role}. Based on the context: "{context}", your task is to: {task}.

**Expected Response Format**:  
- Summary (2-3 lines)  
- Bullet points if applicable  
- Actionable steps or outputs

**Assumptions Made**:  
- The user expects a clear, short response  
- No domain-specific jargon is required  
- Task is intended for general audience
"""

            st.markdown("### ✅ Refined Prompt & Output")
            st.markdown(result)
