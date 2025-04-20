# prompt_generator.py

from openai import OpenAI
from dotenv import load_dotenv
import os

# Load OpenAI API key from .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Create OpenAI client
client = OpenAI(api_key=api_key)

def generate_optimized_prompt(task_description, model="gpt-3.5-turbo"):
    """
    Generate a custom GPT prompt from a simple task description.

    Args:
        task_description (str): A single sentence describing the task.
        model (str): The OpenAI model to use ("gpt-3.5-turbo" or "gpt-4").

    Returns:
        str: An efficient and focused prompt generated for GPT to use.
    """

    system_prompt = (
        "You are a prompt engineering assistant. "
        "Given a short task description, your job is to generate a clear, focused, and optimized prompt "
        "that can be used with GPT models for best performance. Keep it concise but specific."
    )

    user_prompt = f"Task description: {task_description}\n\nGenerate a concise, effective prompt."

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.4,
            max_tokens=300
        )

        optimized_prompt = response.choices[0].message.content.strip()
        return optimized_prompt

    except Exception as e:
        return f"Error: {e}"


# Example usage
if __name__ == "__main__":
    # Replace this with any task you want
    task = input("Describe your task in one sentence: ").strip()
    model_choice = input("Model (gpt-3.5-turbo / gpt-4): ").strip() or "gpt-3.5-turbo"

    result = generate_optimized_prompt(task, model=model_choice)
    print("\n🧠 Optimized Prompt:\n")
    print(result)
