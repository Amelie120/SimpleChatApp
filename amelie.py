import os
import streamlit as st
from langchain_community.llms import OpenAI
from dotenv import load_dotenv
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load the .env file from the current directory
load_dotenv()


def get_openai_response(question):
    try:
        # Use the correct environment variable name
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            logger.error("API key not found in environment variables")
            return "Error: OpenAI API key not found. Please check your .env file."

        # Initialize OpenAI instance
        llm = OpenAI(
            openai_api_key=api_key,
            model_name="gpt-3.5-turbo-instruct",
            temperature=0.9
        )

        response = llm(question)
        return response

    except Exception as e:
        logger.error(f"Error in get_openai_response: {str(e)}")
        return f"An error occurred: {str(e)}"


# Initialize Streamlit app
st.set_page_config(page_title="Q&A Demo")
st.header("Langchain Application")

# Add API key status check
api_status = "✅ API Key Found" if os.getenv(
    "OPENAI_API_KEY") else "❌ API Key Missing"
st.sidebar.write(f"API Status: {api_status}")

user_input = st.text_input("Input: ", key="input")
submit = st.button("Ask the question")

# If ask button is clicked
if submit:
    if user_input.strip():
        with st.spinner('Getting response...'):
            response = get_openai_response(user_input)
            st.subheader("The Response is")
            st.write(response)
    else:
        st.warning("Please enter a question first!")
