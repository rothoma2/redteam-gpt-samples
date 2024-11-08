from openai import OpenAI
import os

# Retrieve API key from environment variable
API_KEY = os.getenv('OPENAI_API_KEY')

if not API_KEY:
    raise ValueError("No OpenAI API key found in environment variables.")

client = OpenAI(api_key=API_KEY)
# Set up the OpenAI API key

def run_prompt(prompt, model="gpt-4o"):
    try:
        completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpfull assistant."},
            {"role": "user", "content": prompt}
        ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return str(e)


if __name__ == "__main__":
    prompt = ("Say Hello Back"
              "")
    response = run_prompt(prompt)
    print(f"Response: {response}")

