import streamlit as st
import openai

# --- Page Config ---
st.set_page_config(page_title="🎯 Prompt Refiner", layout="wide")

# --- CSS Styling ---
st.markdown("""
    <style>
    body {
        background-color: #f5f7fa;
        color: #333333;
        font-family: 'Segoe UI', sans-serif;
    }
    .chat-bubble {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 1rem;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- Session State for Chat History ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Sidebar: API key + History ---
with st.sidebar:
    st.title("🔐 API Setup & History")

    api_key_input = st.text_input("Enter your OpenAI API Key", type="password")
    if api_key_input:
        client = openai.OpenAI(api_key=api_key_input)
    else:
        st.warning("⚠️ Please enter your OpenAI API key to use the app.")

    st.markdown("---")
    st.markdown("### 💬 Chat History")
    if st.session_state.chat_history:
        for idx, chat in enumerate(reversed(st.session_state.chat_history[-10:])):
            with st.expander(f"Prompt #{len(st.session_state.chat_history) - idx}"):
                st.markdown(f"**🧑 Role**: {chat['role']}")
                st.markdown(f"**✅ Task**: {chat['task']}")
                st.markdown(f"**🧠 Response**:\n\n{chat['output']}")
    else:
        st.info("No chats yet. Submit a prompt to see history.")

# --- Main Title ---
st.title("🎯 AI Prompt Refiner")
st.write("Refine your instructions for ChatGPT based on role, context, and task.")

# --- Prompt Form with Examples ---
with st.form("prompt_form"):
    role = st.text_input(
        "🧑 Role",
        placeholder="e.g., Career Coach"
    )
    context = st.text_area(
        "📄 Context (optional)",
        placeholder="e.g., You're helping mid-career professionals switch to the tech industry."
    )
    task = st.text_area(
        "✅ Task",
        placeholder="e.g., Suggest 3 reflection questions to help a user think about their strengths."
    )
    submitted = st.form_submit_button("✨ Refine Prompt")

# --- Handle Submission ---
if submitted:
    if not api_key_input:
        st.error("Please enter your OpenAI API Key in the sidebar.")
    elif not role or not task:
        st.warning("Please fill both Role and Task.")
    else:
        with st.spinner("🔄 Talking to GPT-3.5..."):
            try:
                # System message for GPT
                system_message = """
You are a Prompt Engineer. Given a Role, Context, and Task, your job is to:
- Rewrite a short and effective prompt for GPT use
- Specify the expected response format
- List any assumptions made

Be clear, concise, and helpful.
                """.strip()

                user_input = f"Role: {role}\nContext: {context}\nTask: {task}"

                # API Call (new syntax)
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": system_message},
                        {"role": "user", "content": user_input}
                    ],
                    temperature=0.5
                )

                output = response.choices[0].message.content.strip()

                # Store in history
                st.session_state.chat_history.append({
                    "role": role,
                    "task": task,
                    "output": output
                })

                # Show output
                st.markdown("### 🧠 Refined Output")
                st.markdown(f"<div class='chat-bubble'>{output}</div>", unsafe_allow_html=True)

            except Exception as e:
                st.error(f"⚠️ Error: {e}")
