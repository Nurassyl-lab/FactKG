import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

def main():
    # Retrieve API key from environment variable
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: The environment variable OPENAI_API_KEY is not set.")
        return

    # Initialize the OpenAI client
    client = OpenAI(api_key=api_key)

    # Display library version
    try:
        import openai as _oa
        version = _oa.__version__
    except Exception:
        version = "unknown"
    print(f"Using openai version: {version}")

    # Read prompt from user input
    prompt = input("Enter your prompt: ")
    if not prompt.strip():
        print("No prompt entered. Exiting.")
        return

    # Call the ChatGPT API using the new v1.x interface
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
    except Exception as e:
        print(f"An error occurred while calling the OpenAI API: {e}")
        return

    # Extract and display the assistant's reply
    try:
        assistant_message = response.choices[0].message.content
    except Exception:
        assistant_message = str(response)

    print("\nChatGPT response:\n")
    print(assistant_message)

if __name__ == "__main__":
    main()
