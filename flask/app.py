GROQ_API_KEY = "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"
from flask import Flask, request, jsonify
from flask_cors import CORS 
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
import json

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'

CORS(app)  


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
        

        
        
    # # Manually return the sample quiz in JSON format for debugging purposes
    #     sample_quiz = [
    #         {
    #             "id": 1,
    #             "question": "What is the primary criterion used to estimate regression coefficients in a simple linear regression model?",
    #             "options": [
    #                 "Mean Absolute Deviation",
    #                 "Least Squares Criterion",
    #                 "Mean Squared Error",
    #                 "Coefficient of Determination"
    #             ],
    #             "correctAnswer": 1,
    #             "explanation": "The least squares criterion is used to estimate regression coefficients in a simple linear regression model. It minimizes the sum of the squared differences between the observed and predicted values of the dependent variable."
    #         },
    #         {
    #             "id": 2,
    #             "question": "What is the purpose of residual plots in simple linear regression analysis?",
    #             "options": [
    #                 "To estimate regression coefficients",
    #                 "To calculate the coefficient of determination",
    #                 "To indicate if assumptions of the model have been violated",
    #                 "To formulate tests of fit"
    #             ],
    #             "correctAnswer": 2,
    #             "explanation": "Residual plots are used to indicate if the assumptions of the simple linear regression model have been violated. They help to identify patterns or non-randomness in the residuals, which can suggest that the model is not appropriate for the data."
    #         },
    #         {
    #             "id": 3,
    #             "question": "What is the primary use of Analysis of Variance (ANOVA) in regression analysis?",
    #             "options": [
    #                 "To estimate regression coefficients",
    #                 "To calculate the coefficient of determination",
    #                 "To formulate tests of fit and of regression coefficients",
    #                 "To minimize the sum of the squared differences between the observed and predicted values"
    #             ],
    #             "correctAnswer": 2,
    #             "explanation": "Analysis of Variance (ANOVA) is used to formulate tests of fit and of regression coefficients in regression analysis. It helps to determine whether the regression model is significant and whether the independent variable(s) have a significant effect on the dependent variable."
    #         },
    #         {
    #             "id": 4,
    #             "question": "What is the standard error of estimate used for in simple linear regression?",
    #             "options": [
    #                 "To calculate the coefficient of determination",
    #                 "To estimate regression coefficients",
    #                 "To formulate tests of fit",
    #                 "To measure the variability of the dependent variable around the regression line"
    #             ],
    #             "correctAnswer": 3,
    #             "explanation": "The standard error of estimate is used to measure the variability of the dependent variable around the regression line in simple linear regression. It provides a measure of the uncertainty of predictions made using the regression model."
    #         }
    #     ]
        
    #     return jsonify(sample_quiz), 200


    
    

    except Exception as e:
        return jsonify({"error": f"Error processing file: {str(e)}"}), 500

    finally:
        # Clean up the uploaded file
        if os.path.exists(file_path):
            os.remove(file_path)

if __name__ == '__main__':
    app.run(debug=True, port=8000)
