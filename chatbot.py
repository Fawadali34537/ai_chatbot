import streamlit as st
import json
import openai  # OpenAI API
import os

# Load FAQs
with open("faq_dataset.json", "r") as file:
    faq_data = json.load(file)

# Load document for RAG
with open("sample_doc.txt", "r") as file:
    document_text = file.read()

# Set OpenAI API Key (Replace with your actual key)
openai.api_key = "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"

def get_faq_answer(user_query):
    """Check if query matches predefined FAQs."""
    for faq in faq_data:
        if user_query.lower() in faq["question"].lower():
            return faq["answer"]
    return None

def ask_ai_agent(query):
    """Send query to OpenAI API or Ollama."""
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Change to "ollama" if using locally
        messages=[
            {"role": "system", "content": "You are a helpful AI agent."},
            {"role": "user", "content": f"User Query: {query}\nRelevant Document: {document_text}"}
        ]
    )
    return response["choices"][0]["message"]["content"]

# Streamlit UI
st.title("🤖 AI Chatbot with RAG & FAQs")

# Create a dropdown for the user to select a question from the dataset
questions = [faq["question"] for faq in faq_data]
selected_question = st.selectbox("Select a question:", questions)

if selected_question:
    # Get the answer to the selected question from the FAQ dataset
    faq_response = get_faq_answer(selected_question)
    
    if faq_response:
        st.success(f"✅ **FAQ Answer:** {faq_response}")
    else:
        # Use AI agent if no FAQ match
        ai_response = ask_ai_agent(selected_question)
        st.info(f"🤖 **AI Response:** {ai_response}")
