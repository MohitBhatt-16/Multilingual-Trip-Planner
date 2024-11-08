import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_groq import ChatGroq
from langdetect import detect
from deep_translator import GoogleTranslator
from main import TripCrew, TripAnswer
from dotenv import load_dotenv
from markdownify import markdownify as md_to_text
from datetime import date

# Get today's date
today = date.today()

# Print today's date
print("Today's date is:", today)


# Initialize the LLM
load_dotenv()
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

# Initialize the Streamlit App
st.title('_NextTrip.AI_ :sunglasses:')
st.title("Plan your next adventure with ease!")

if "initialized" not in st.session_state:
    st.session_state["initialized"] = False
    st.session_state["trip_details"] = {}

user_input = st.text_input("You:", key="user_input")

if st.button("Send"):
    if not st.session_state["initialized"]:
        extracted_info, source_language = process_input(user_input)
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

        # Store trip details
        st.session_state["trip_details"] = {
            "origin": origin, "destination": destination, "number_of_days": number_of_days,
            "number_of_adults": number_of_adults, "number_of_children": number_of_children,
            "budget": budget, "date_range": date_range, "interests": interests
        }

        trip_crew = TripCrew(origin, number_of_days, destination, date_range, interests, budget, number_of_children, number_of_adults)
        result = trip_crew.run()
        
        heading = translate_to_regional("Here is your whole trip plan specifically customized as per your choice", source_language)
        st.subheader(heading)
        markdown_text = str(result)
        translated_result = translate_to_regional(markdown_text, source_language)
        st.markdown(translated_result, unsafe_allow_html=True)
        
        st.session_state["initialized"] = True

    else:
        source_language = detect_language(user_input)
        english_prompt = translate_to_english(user_input, source_language)

        trip_answer = TripAnswer(
            origin=st.session_state["trip_details"]["origin"],
            destination=st.session_state["trip_details"]["destination"],
            interests=st.session_state["trip_details"]["interests"],
            no_of_days=st.session_state["trip_details"]["number_of_days"],
            date_range=st.session_state["trip_details"]["date_range"],
            budget=st.session_state["trip_details"]["budget"],
            no_of_child=st.session_state["trip_details"]["number_of_children"],
            no_of_adults=st.session_state["trip_details"]["number_of_adults"],
            query=english_prompt
        )
        result = trip_answer.run()
        markdown_text = str(result)
        translated_result = translate_to_regional(markdown_text, source_language)
        st.markdown(translated_result, unsafe_allow_html=True)
