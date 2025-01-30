
from flask import Flask, request, jsonify
from flask_cors import CORS 
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
import json


GROQ_API_KEY=os.getenv("GROQ_API_KEY")

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'

CORS(app, resources={r"/generate-quiz": {"origins": "https://quiz-genie-pdf-to-quiz.vercel.app"}})
# CORS(app) 


# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# LangChain prompt template for quiz generation
prompt_template = """
You are a quiz creator. Based on the following content, generate a JSON quiz containing 3-5 multiple-choice questions. 
Each question should have 4 options, 1 correct answer, and a clear explanation.Give 8-10 questions.

Content: {content}

Output format:
[
    {{
        "id": 1,
        "question": "Question text",
        "options": ["Option A", "Option B", "Option C", "Option D"],
        "correctAnswer": 1,  // Index of the correct answer
        "explanation": "Explanation of the correct answer."
    }},
    ...
]
"""

import re
def extract_json_from_response(response):
    """
    Extracts JSON content from the LLM response safely.
    Handles cases where the response is an AIMessage object.
    """
    if isinstance(response, dict):  # Sometimes response can be a dict
        response_text = json.dumps(response)
    elif hasattr(response, "content"):  # AIMessage object case
        response_text = response.content
    elif isinstance(response, str):
        response_text = response
    else:
        print(f"Unexpected response type: {type(response)}")
        return None

    # Extract JSON part using regex
    match = re.search(r"\[.*\]", response_text, re.DOTALL)
    if match:
        json_string = match.group(0)  # Extract JSON
        try:
            return json.loads(json_string)  # Convert to Python dict
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return None
    else:
        print("No JSON found in the response.")
        return None





@app.route('/generate-quiz', methods=['POST'])
def generate_quiz():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    if not file.filename.endswith('.pdf'):
        return jsonify({"error": "Invalid file type. Please upload a PDF."}), 400

    # Save the uploaded PDF
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    print(f"Saving file to: {file_path}")  # Debug line
    file.save(file_path)

    try:
        # Load the PDF content using LangChain
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        if not documents:
            return jsonify({"error": "Failed to extract content from PDF"}), 400
        # print(f"Loaded documents: {documents[:2]}")  # Debug line
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        text_chunks = text_splitter.split_documents(documents)

        # Use LangChain's LLM to generate the quiz
        llm = ChatGroq(model='llama3-70b-8192', api_key=GROQ_API_KEY)  # Use your preferred LLM
        prompt = PromptTemplate(input_variables=["content"], template=prompt_template)
        # chain = LLMChain(llm=llm, prompt=prompt)
        chain = prompt | llm

        # Generate quiz questions for the first chunk of content
        content = text_chunks[0].page_content  # You can extend this for more chunks
        quiz_json = chain.invoke(content)
        print(quiz_json)

        quiz_json_cleaned = extract_json_from_response(quiz_json)
        print("Cleaned JSON:", quiz_json_cleaned)

        if not quiz_json_cleaned:
            return jsonify({"error": "No valid JSON found in LLM response"}), 500

        return quiz_json_cleaned,200
        
    except Exception as e:
        return jsonify({"error": f"Error processing file: {str(e)}"}), 500

    finally:
        # Clean up the uploaded file
        if os.path.exists(file_path):
            os.remove(file_path)

if __name__ == '__main__':
    app.run(port=8000)
