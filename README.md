# 🧠 QuizGenie - PDF to Quiz Generator

## 📝 Overview

QuizGenie is an AI-powered application that transforms PDFs into multiple-choice quizzes. With a **Flask backend** and a **React (Vite) frontend**, it extracts key information from documents and generates meaningful quiz questions.

## 🚀 Features

- **PDF Parsing**: Extracts text from PDFs efficiently.
- **AI-Generated Quizzes**: Uses Groq’s **Llama3-70B-8192** model to create quizzes.
- **Customizable Topics**: Generates quizzes based on selected topics.
- **Interactive UI**: Built with React (Vite) for a seamless user experience.

## 🛠️ Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/krishshah9944/QuizGenie-PDF-to-Quiz.git
cd QuizGenie-PDF-to-Quiz
```

### 2️⃣ Backend Setup (Flask)

Navigate to the backend folder:

```bash
cd flask
```

Create a virtual environment and activate it:

For Windows:
```bash
python -m venv venv
venv\Scripts\activate
```
For macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Set up environment variables:
Create a `.env` file in the `flask` directory and add your API key:
```
GROQ_API_KEY=your_api_key_here
```

Run the backend:
```bash
python app.py
```

### 3️⃣ Frontend Setup (React + Vite)

Navigate to the frontend folder:
```bash
cd ../project
```

Install dependencies:
```bash
npm install
```

Start the frontend server:
```bash
npm run dev
```

## 📌 Usage

1. Upload a PDF file.
2. The AI processes the document and generates quiz questions.
3. Review and interact with the generated quiz in the UI.

## 🎥 Demo

Check out the live demo: [QuizGenie App](https://quiz-genie-pdf-to-quiz.vercel.app/)

### ⚠️ Note
- **Processing might take up to 1 minute** due to limited computational power.
- **Large PDFs are not supported** in the demo due to resource constraints.

## 🤝 Contributing

Feel free to contribute by submitting issues or pull requests. Suggestions and improvements are always welcome!

## 📧 Contact

For inquiries, reach out via:

- **LinkedIn**: [Krish Shah](https://www.linkedin.com/in/krishshah9944/)
- **Email**: [krishshah9944@gmail.com](mailto:krishshah9944@gmail.com)

