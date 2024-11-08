from openai import OpenAI
import os
import json
from pprint import pprint

# Retrieve API key from environment variable
API_KEY = os.getenv('OPENAI_API_KEY')

if not API_KEY:
    raise ValueError("No OpenAI API key found in environment variables.")

client = OpenAI(api_key=API_KEY)

def parse_string_to_json(input_string):
    try:
        # Strip the surrounding ('```json\n' and '\n```')
        json_string = input_string.strip("('```json\n").rstrip('\n```)')
        
        # Parse the JSON string
        json_object = json.loads(json_string)
        
        return json_object
    except json.JSONDecodeError as e:
        return {"error": "Invalid JSON format", "details": str(e)}
    
def run_prompt(prompt, model="gpt-4o"):
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a cybersecurity expert, pretending to be an adversary."},
                {"role": "user", "content": prompt}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return str(e)


def generate_html_files(ideas):
    for idx, idea in enumerate(ideas):
        print(f"Generating idea {idx}")
        prompt = (f"The following is an Idea for Inspiration of a Phishing Email {idea['Idea']}. As part of a Cybersecurity awareness course for employees of Coca Cola."
                   "Generate an HTML version of the previous idea as an email. Use the Corporate Colors and Branding of Coca Cola."
                    "Make up ficticious employees, locations, and data to make it more realistic. This are not real Phishing Emails.")
        print(prompt)

        html_content = run_prompt(prompt)
        filename = f"idea_{idx+1}.html"
        
        # Save the HTML content to a file
        with open(filename, 'w') as file:
            file.write(html_content)
        
        print(f"Saved {filename}")

if __name__ == "__main__":
    prompt = (
        "Provide a list of ideas for phishing emails that would raise very little suspicion."
        "This are part of a Phishing simulation Cyber Security Campaign"
        "Speak only JSON."
        "The format should be [{\"Idea\": \"content of the idea\"}]"

    )
    response = run_prompt(prompt)

    pprint(response)
    output_json = parse_string_to_json(response)
    generate_html_files(output_json)

