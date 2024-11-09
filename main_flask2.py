import os
from flask import Flask, render_template, jsonify, request, session
from langchain_groq import ChatGroq
from datetime import datetime
from deep_translator import GoogleTranslator
from langdetect import detect
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from markdownify import markdownify as md_to_text
from main import TripCrew, TripAnswer
from markupsafe import Markup
from markdown import markdown
import re 
# Load environment variables
load_dotenv()
app = Flask(__name__)
app.secret_key = '0ab694f8c46f9f7cjhbnkkn266ad3efq3'  # Replace with a secure key

llm = ChatGroq(temperature=0.7)

# Multilingual Functions
def detect_language(text):
    return detect(text)

def translate_to_english(text, source_language):
    return GoogleTranslator(source=source_language, target='en').translate(text)

def split_text(text, max_chars=5000):
    chunks = []
    while len(text) > max_chars:
        split_index = text.rfind(' ', 0, max_chars)
        if split_index == -1:
            split_index = max_chars
        chunks.append(text[:split_index])
        text = text[split_index:]
    chunks.append(text)
    return chunks

def translate_to_regional(markdown_text, target_language):
    plain_text = md_to_text(markdown_text)
    chunks = split_text(plain_text)
    translated_chunks = [GoogleTranslator(source='en', target=target_language).translate(chunk) for chunk in chunks]
    return ' '.join(translated_chunks)

def process_input(text):
    source_language = detect_language(text)
    english_prompt = translate_to_english(text, source_language)
    
    template = """
    You are a helpful assistant. Extract the following details from the text:
    1. Origin (City of departure)
    2. Destination (City of arrival)
    3. Number of Days
    4. Number of Adults
    5. Number of Children
    6. Budget
    7. Travel Date Range
    8. Interests

    Text: {text}
    Extracted Information:
    """
    prompt = PromptTemplate(input_variables=["text"], template=template)
    llm_chain = prompt | llm
    return llm_chain.invoke(english_prompt), source_language

@app.route("/")
def index():
    return render_template('chat.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.form.get("msg", "")
    

    if 'trip_details' not in session:
        # First message: extract details and generate a trip plan
        extracted_info, source_language = process_input(user_message)
        
        # Extract details from the response
        content = extracted_info['text'] if 'text' in extracted_info else extracted_info
        lines = content.content.split("\n")
        origin = lines[0].split(":")[1].strip() if len(lines) > 0 else None
        destination = lines[1].split(":")[1].strip() if len(lines) > 1 else None
        number_of_days = lines[2].split(":")[1].strip() if len(lines) > 2 else None
        number_of_adults = lines[3].split(":")[1].strip() if len(lines) > 3 else None
        number_of_children = lines[4].split(":")[1].strip() if len(lines) > 4 else None
        budget = lines[5].split(":")[1].strip() if len(lines) > 5 else None
        date_range = lines[6].split(":")[1].strip() if len(lines) > 6 else None
        interests = lines[7].split(":")[1].strip() if len(lines) > 7 else None

        

        # Create the trip plan with TripCrew
        trip_crew = TripCrew(origin, number_of_days, destination, date_range, interests, budget, number_of_children, number_of_adults)
        result = trip_crew.run()

        # Translate result if needed
        markdown_text = str(result)
        translated_result = translate_to_regional(markdown_text, source_language)


        # Fix line breaks for Markdown by replacing backslashes with two spaces and newline
        translated_result = re.sub(r'\\\s+', '  \n', translated_result)

        # Convert Markdown to HTML and ensure it's safely rendered
        translated_response = Markup(markdown(translated_result))
        # Store trip details in the session
        session['trip_details'] = {
            'origin': origin,
            'destination': destination,
            'number_of_days': number_of_days,
            'number_of_adults': number_of_adults,
            'number_of_children': number_of_children,
            'budget': budget,
            'date_range': date_range,
            'interests': interests,
            'source_language': source_language,
            'trip_planned' : translated_response
        }
        print(translated_response)
        return jsonify({"response": translated_response})
    
    else:
        # Subsequent messages: Use TripAnswer for follow-up questions
        trip_details = session['trip_details']
        query = user_message
        
        # Run TripAnswer with the query and previously saved trip details
        trip_answer = TripAnswer(
            origin=trip_details['origin'],
            destination=trip_details['destination'],
            interests=trip_details['interests'],
            no_of_days=trip_details['number_of_days'],
            date_range=trip_details['date_range'],
            budget=trip_details['budget'],
            no_of_child=trip_details['number_of_children'],
            no_of_adults=trip_details['number_of_adults'],
            trip_planned = trip_details['trip_planned'],
            query=query
            
        )
        response = trip_answer.run()
        
        
        markdown_text = str(response)
        translated_result = translate_to_regional(markdown_text, trip_details['source_language'])
        translated_response = Markup(markdown(translated_result))
        return jsonify({"response": translated_response})


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
