from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
import os
import json
import streamlit as st

load_dotenv(override= True)

# Works both locally and on Streamlit Cloud
def get_secret(key):
    try:
        return st.secrets[key]
    except:
        return get_secret(key)


SYSTEM_PROMPT = """You are a freight inquiry assistant for ABC International Logistics Karachi.


STEP 11:
- If customer says YES → Say exactly: "Thank you! Your reference number is FR-2026-[random 4 digits]. Our team will contact you within 5 minutes."
- If customer says NO → Ask "What would you like to correct?"

NEVER send reference number before customer confirms with YES."""



def run_agent(user_input: str, chat_history: list) -> str:
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.3,
        api_key=get_secret("GROQ_API_KEY")
    )

    system_message = SystemMessage(content=SYSTEM_PROMPT)
    messages = [system_message] + chat_history + [HumanMessage(content=user_input)]
    response = llm.invoke(messages)
    return response.content

def extract_inquiry_details(chat_history: list) -> dict:
    """Extract all collected details from chat history into structured format"""
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
        api_key=get_secret("GROQ_API_KEY")
    )

     # Convert chat history to readable text
    conversation_text = ""
    for message in chat_history: 
        if hasattr(message, 'content'):
            if message.__class__.__name__ == 'HumanMessage':
                conversation_text += f"Customer: {message.content}\n"
            elif message.__class__.__name__ == 'AIMessage':
                conversation_text += f"Assistant: {message.content}\n"

    extraction_prompt = f"""Extract all freight inquiry details from this conversation 
    and return ONLY a valid JSON object. 
    
    Look carefully through the entire conversation for these details.
    If a field is not mentioned, use empty string "".

    Return this exact JSON structure:
    {{
        "customer_name": "extracted name or empty",
        "company_name": "extracted company or empty",
        "email": "extracted email or empty",
        "phone": "extracted phone or empty",
        "shipment_direction": "Import or Export",
        "services required": "extracted services or empty",
        "select the country": "extracted company name or empty",
        "message": "customer message",
        "reference_number": "extracted reference number or FR-2026-0001",
        "status": "pending"
    }}

    Conversation to analyze:
    {conversation_text}

    IMPORTANT: Return ONLY the JSON object. No explanation. No markdown. No backticks."""

    response = llm.invoke([HumanMessage(content=extraction_prompt)])

    try:
        # Clean response
        content = response.content.strip()
        # Remove markdown if present
        if "```" in content:
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
        details = json.loads(content.strip())
        return details
    except Exception as e:
        print(f"Extraction error: {e}")
        print(f"Raw response: {response.content}")
        return {}
