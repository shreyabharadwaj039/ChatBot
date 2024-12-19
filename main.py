import google.generativeai as genai
from dotenv import load_dotenv
import os
import streamlit as st

# Load environment variables from .env file
load_dotenv()

def generate_response(query):
    """
    Generate a response using the Google Gemini model.
    """
    try:
        # Load API key from environment variables
        api_key = os.getenv("GEMINI")
        if not api_key:
            raise ValueError("API key is missing. Ensure GEMINI_API_KEY is set in the .env file.")

        # Configure the Gemini API with the API key
        genai.configure(api_key=api_key)

        # Model generation configuration
        generation_config = {
            "temperature": 0.9,  # Creativity level
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,  # Max response length
        }

        # Safety settings
        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
        ]

        # Initialize the Gemini model
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",  # Ensure this is the correct model name
            generation_config=generation_config,
            safety_settings=safety_settings
        )

        # Start a conversation (optional for context-based conversations)
        convo = model.start_chat(history=[])

        # Construct the prompt for the model
        prompt = f"""
        Answer the below query:

        Query:
        {query}
        """

        # Send the message to the model
        convo.send_message(prompt)

        # Generate the response
        response = convo.last.text
        return response

    except Exception as e:
        return f"Error generating response: {e}"

# Streamlit app
st.title("Simple Chatbot with GenAI")
st.write("Hi, Welcome to the RAIT Chatbot!")

# Text input for the user query
query = st.text_input("Enter your query: ")

# When the "Generate Answer" button is pressed, generate the response
if st.button("Generate Answer"):
    if query:
        with st.spinner("Processing your query..."):
            insights = generate_response(query)
            st.write("Insights:")
            st.write(insights)
    else:
        st.write("Please enter a query to get a response.")