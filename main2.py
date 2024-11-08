import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_groq import ChatGroq
from langdetect import detect
from deep_translator import GoogleTranslator
from main import TripCrew, TripAnswer
from dotenv import load_dotenv
from markdownify import markdownify as md_to_text
# from tools_created.search_tools import imp_links
# from web_text import extract_text


# Initialize the LLM (or other LLMs you prefer)
load_dotenv()
llm = ChatGroq(temperature=0.7)


### Multilingual
def detect_language(text):
    """Detect the language of the input text."""
    return detect(text)

def translate_to_english(text, source_language):
    """Translate the regional language to English using deep-translator."""
    return GoogleTranslator(source=source_language, target='en').translate(text)

#def translate_to_regional(text, target_language):
    # """Translate the English response back to the regional language using deep-translator."""
    # return GoogleTranslator(source='en', target=target_language).translate(text)

def split_text(text, max_chars=5000):
    chunks = []
    while len(text) > max_chars:
        # Find the last space within the allowed limit to avoid cutting in the middle of a word
        split_index = text.rfind(' ', 0, max_chars)
        if split_index == -1:
            split_index = max_chars  # If no space is found, just split at the limit
        chunks.append(text[:split_index])
        text = text[split_index:]
    chunks.append(text)  # Add the remaining part of the text
    return chunks

def translate_to_regional(markdown_text, target_language):
    # Convert the Markdown content to plain text
    plain_text = md_to_text(markdown_text)
    
    # Split the plain text into chunks for translation if it exceeds 5000 characters
    chunks = split_text(plain_text)
    
    translated_chunks = []
    
    # Translate each chunk
    for chunk in chunks:
        translated_chunk = GoogleTranslator(source='en', target=target_language).translate(chunk)
        translated_chunks.append(translated_chunk)
    
    # Join all translated chunks back together
    return ' '.join(translated_chunks)

def process_input(text):
    """End-to-end process: detect language, translate, query LLM, translate back."""
    # Step 1: Detect the language
    source_language = detect_language(text)
    print(f"Detected language: {source_language}")
    
    # Step 2: Translate input to English
    english_prompt = translate_to_english(text, source_language)
    print(f"Translated to English: {english_prompt}")
    
    # Define the prompt template for extracting travel details and interests
    template = """
    You are a helpful assistant. Extract the following details from the text:

    1. Origin (City of departure)
    2. Destination (City of arrival)
    3. Number of Days
    4. Number of Adults
    5. Number of Children
    6. Budget (in dollars or other currency)
    7. Travel Date Range (Start and End Date combined in the form of a range)
    8. Interests (all the interests mentioned by the user, such as hiking, swimming, sightseeing, etc. seperated by comma ',')

    Text: {text}

    Extracted Information:
    """

    prompt = PromptTemplate(
        input_variables=["text"],
        template=template,
    )

    # Set up the LangChain with the LLM and prompt
    llm_chain = prompt | llm
    return llm_chain.invoke(english_prompt),source_language
    





st.title('_NextTrip.AI_ :sunglasses:')
st.title("Plan your next adventure with ease!")

# Initialize session state for storing the conversation
# if "history" not in st.session_state:
#     st.session_state.history = []

# User input
user_input = st.text_input("You:", key="user_input")
but = st.button("Send")
if but:
    # Append the user input to the conversation history
    # st.session_state.history.append({"user": user_input})
    print("inside 0 ")
    # Extract the information using LangChain
    extracted_info,source_language = process_input(user_input)

    # Assuming the response is in a format that can be split into variables
    content = extracted_info['text'] if 'text' in extracted_info else extracted_info

    # Split the content into parts based on your predefined structure
    # We assume the LLM outputs the information in a clear structured way
    lines = content.content.split("\n")
    print(lines)

    # Extract relevant details into variables
    origin = lines[0].split(":")[1].strip().split()[0] if len(lines) > 0 else None
    destination = lines[1].split(":")[1].strip().split()[0] if len(lines) > 1 else None
    number_of_days = lines[2].split(":")[1].strip().split()[0] if len(lines) > 2 else None
    number_of_adults = lines[3].split(":")[1].strip().split()[0] if len(lines) > 3 else None
    number_of_children = lines[4].split(":")[1].strip().split()[0] if len(lines) > 4 else None
    budget = lines[5].split(":")[1].strip() if len(lines) > 5 else None
    date_range = lines[6].split(":")[1].strip() if len(lines) > 6 else None
    interests = lines[7].split(":")[1].strip() if len(lines) > 7 else None


    trip_crew = TripCrew(origin,number_of_days, destination, date_range, interests,budget, number_of_children,number_of_adults)
    result = trip_crew.run()
    print(type(result))
    heading = translate_to_regional('Here is your whole trip plan specifically customized as per your choice',source_language)
    st.subheader(heading)
    # print(result)
    # Convert CrewOutput object to a string
    markdown_text = str(result)

    new = translate_to_regional(markdown_text ,source_language)
    # text_html = new.replace("**", "<b>").replace("**", "</b>", 1)
    st.markdown(new, unsafe_allow_html=True)
    print("Ended")
    i=1
    but = False

    # # File to save the extracted text
    # output_file = 'extracted_texts.txt'
    # print(imp_links)
    # # Open the file in write mode
    # with open(output_file, 'w', encoding='utf-8') as file:
    #     # Loop through URLs and extract text for each one
    #     for url in imp_links:
    #         text = extract_text(url)
    #         if text:
    #             # Write the URL and corresponding text to the file
    #             file.write(f"Text for {url}:\n")
    #             file.write(text)
    #             file.write("\n" + "="*80 + "\n\n")  # Add a separator between pages

    # print(f"Text extracted and saved in {output_fil