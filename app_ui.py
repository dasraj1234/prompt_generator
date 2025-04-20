# -----------------------------
# 📦 Import necessary libraries
# -----------------------------
import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

# --------------------------------------------
# 🔐 Load your OpenAI API key from the .env file
# --------------------------------------------
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# --------------------------------------------------------
# 🤖 Initialize the OpenAI client with the loaded API key
# --------------------------------------------------------
client = OpenAI(api_key=api_key)

# ----------------------------------------------------------
# 🧠 Define your custom reusable GPT prompt as a template
# ----------------------------------------------------------
custom_prompt_template = """
You are an expert GPT prompt engineer.

Your task is to create a reusable, well-structured GPT prompt that can be used repeatedly to generate content for a specific task.

Given the task below, generate a prompt that:
- Tells the GPT model what kind of role it should take (e.g., expert, teacher, creator, etc.)
- Clearly explains what kind of content should be generated
- Includes formatting and style guidance
- Uses a variable placeholder like {input} or {topic} so the prompt can be reused for different inputs
- Is written clearly and cleanly, ready to be copy-pasted into a GPT interface

Task: <<<TOPIC>>>

Return only the reusable GPT prompt with {input} in place of any user topic or content.
"""

# ------------------------------------------------------
# 🛠️ Function to replace placeholder and call the GPT API
# ------------------------------------------------------
def generate_instructions(user_topic, prompt_template):
    final_prompt = prompt_template.replace("<<<TOPIC>>>", user_topic.strip())

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": final_prompt}
        ],
        temperature=0.7,
        max_tokens=1000
    )

    return response.choices[0].message.content


# -------------------------------------
# 🚀 Build the Streamlit web interface
# -------------------------------------
# Use wide layout for full screen width
st.set_page_config(page_title="GPT Prompt Generator", layout="wide")

# Page title and intro
st.title("🧠 Reusable GPT Prompt Generator")
st.markdown("""
Welcome! 👋  
Enter a task you'd like to automate using GPT (e.g., *write a blog post*, *summarize a video*, etc.).  
This app will generate a **reusable GPT prompt** with a `{input}` placeholder that you can use again and again!
""")

# Input area
user_topic = st.text_area("✍️ Describe the task GPT should help with:", height=100, placeholder="e.g., Write a professional LinkedIn post from a given topic")

# Button to trigger generation
if st.button("⚡ Generate Reusable Prompt"):
    if user_topic.strip() == "":
        st.warning("Please enter a task before generating the prompt.")
    else:
        with st.spinner("Generating your prompt..."):
            output = generate_instructions(user_topic, custom_prompt_template)

        # Scrollable, full-width output box
        st.subheader("✅ Your Reusable GPT Prompt:")
        st.text_area("",
                     value=output,
                     height=400,
                     label_visibility="collapsed",
                     key="output_prompt",
                     help="Scroll to view the full prompt")

# Footer
st.markdown("---")
st.caption("Built with ❤️ using Streamlit and OpenAI.")
