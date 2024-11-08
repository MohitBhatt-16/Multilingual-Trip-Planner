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
from datetime import datetime
from deep_translator import GoogleTranslator
from langdetect import detect
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from markdownify import markdownify as md_to_text

load_dotenv()
llm = ChatGroq(temperature=0.7)

template = """Give me answer to the question.
Question : {question}"""

prompt = PromptTemplate(
    input_variables=['question'],
    template = template,
)
llm_chain = prompt | llm

### Multilingual part
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

# def translate_to_regional(markdown_text, target_language):
#     plain_text = str(markdown_text)
#     # Split the plain text into chunks for translation if it exceeds 5000 characters
#     chunks = split_text(plain_text)
    
#     translated_chunks = []
    
#     # Translate each chunk
#     for chunk in chunks:
#         translated_chunk = GoogleTranslator(source='en', target=target_language).translate(chunk)
#         translated_chunks.append(translated_chunk)
    
#     # Join all translated chunks back together
#     return ' '.join(translated_chunks)


def translate_to_regional(text, target_language):
    """Translate the English response back to the regional language using deep-translator."""
    return GoogleTranslator(source='en', target=target_language).translate(text)




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

    if image_file:
        # Generate a unique filename based on the current timestamp
        filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{image_file.filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Save the image
        image_file.save(filepath)
        
        # Set response message with image path
        response_message = f"<img src='/static/uploads/{filename}' alt='Uploaded Image' style='max-width: 450px; width: 100%; height: auto; border-radius: 5px; margin: 0px 0;' />"
    elif user_message:
        detected_language = detect_language(user_message)
        converted_msg = translate_to_english(user_message, detected_language)
        response_from_gpt = llm_chain.invoke(converted_msg)
        print(response_from_gpt.content)
        print(detected_language)
        respond = translate_to_regional(response_from_gpt.content,detected_language)
        response_message = f"{respond}"

    return jsonify({"response": response_message})

if __name__ == '__main__':
    app.run(debug=True)