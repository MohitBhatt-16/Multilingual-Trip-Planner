# from src.helper import embedding_model
# from langchain_community.vectorstores import Pinecone as PineconeStore
# from dotenv import load_dotenv
# from src.prompt import *
# from langchain.chains import RetrievalQA
# from langchain_core.prompts import PromptTemplate
import os
from flask import Flask, render_template, jsonify, request
from langchain_groq import ChatGroq
from flask import Flask
# from pinecone import Pinecone
from PIL import Image
import io
from main import TripCrew, TripAnswer
from datetime import datetime
from deep_translator import GoogleTranslator
from langdetect import detect
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from markdownify import markdownify as md_to_text

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








app = Flask(__name__)

# load_dotenv()

# PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
# GROQ_API_KEY = os.environ.get('GROQ_API_KEY')

# embeddings = embedding_model()

# pinecone = Pinecone(api_key=PINECONE_API_KEY)

index_name = "medical-chatbot"

# docsearch = PineconeStore.from_existing_index(index_name,embeddings)

# PROMPT = PromptTemplate(template=prompt_template,input_variables=["context","question"])
# chain_type_kwargs = {"prompt":PROMPT}

# llm = ChatGroq(model="mixtral-8x7b-32768")

# qa = RetrievalQA.from_chain_type(
#     llm = llm,
#     chain_type = 'stuff',
#     retriever = docsearch.as_retriever(search_kwargs = {'k':2}),
#     return_source_documents = True,
#     chain_type_kwargs = chain_type_kwargs
# )

@app.route("/")
def index():
    return render_template('chat.html')

# @app.route("/get",methods = ["GET","POST"])
# def chat():
#     msg = request.form["msg"]
#     input = msg
#     print(input)
    # result = qa({"query":input})
    # print("Response : ", result["result"])
    # return str(result["result"])

# Folder to save uploaded images temporarily
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.form.get("msg", "")
    image_file = request.files.get("image")
    response_message = ""

    extracted_info, source_language = process_input(user_message)
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

    trip_crew = TripCrew(origin, number_of_days, destination, date_range, interests, budget, number_of_children, number_of_adults)
    result = trip_crew.run()
        
    # heading = translate_to_regional("Here is your whole trip plan specifically customized as per your choice", source_language)
    # st.subheader(heading)
    markdown_text = str(result)
    translated_result = translate_to_regional(markdown_text, source_language)
    
        

    return jsonify({"response": translated_result})

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)