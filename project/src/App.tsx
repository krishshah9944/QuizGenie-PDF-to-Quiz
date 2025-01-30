
import React, { useState } from "react";
import axios from "axios";
import { questions, type QuizResult, type Question } from "./data/questions";
import { ArrowRight, RefreshCw, Upload } from "lucide-react";

function App() {
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState<number | null>(null);
  const [quizCompleted, setQuizCompleted] = useState(false);
  const [quizResults, setQuizResults] = useState<QuizResult[]>([]);
  const [questionsState, setQuestionsState] = useState<Question[]>(questions);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleAnswerSelect = (index: number) => {
    if (selectedAnswer === null) {
      setSelectedAnswer(index);
      setQuizResults((prev) => [
        ...prev,
        {
          questionId: questionsState[currentQuestion].id,
          userAnswer: index,
          isCorrect: index === questionsState[currentQuestion].correctAnswer,
          correctAnswer: questionsState[currentQuestion].correctAnswer,  // Store correct answer
          explanation: questionsState[currentQuestion].explanation,      // Store explanation
        },
      ]);
    }
  };
  

  const handleNext = () => {
    if (currentQuestion < questionsState.length - 1) {
      setCurrentQuestion((prev) => prev + 1);
      setSelectedAnswer(null);
    } else {
      setQuizCompleted(true);
    }
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      const formData = new FormData();
      formData.append("file", file);

      try {
        setUploading(true);
        setError(null);

        const response = await axios.post(
          "http://127.0.0.1:8000/generate-quiz",
          formData,
          { headers: { "Content-Type": "multipart/form-data" } }
        );

        setQuestionsState(response.data);
        setQuizResults([]);
        setQuizCompleted(false);
        setCurrentQuestion(0);
      } catch (err) {
        console.error("Error uploading file:", err);
        setError(`Failed to generate quiz. Error: ${err}`);
      } finally {
        setUploading(false);
      }
    }
  };

  const calculateScore = () => {
    const correctAnswers = quizResults.filter((result) => result.isCorrect).length;
    return {
      score: correctAnswers,
      total: questionsState.length,
      percentage: Math.round((correctAnswers / questionsState.length) * 100),
    };
  };

  const renderUploadSection = () => (
    <div className="bg-white rounded-2xl shadow-xl p-8 text-center mb-6">
      <div className="flex flex-col items-center">
        <Upload className="w-12 h-12 text-indigo-600 mb-4" />
        <h2 className="text-2xl font-bold text-gray-800 mb-2">Upload a PDF</h2>
        <p className="text-gray-600 mb-4">Provide a PDF file to generate a quiz.</p>
        <input
          type="file"
          accept="application/pdf"
          onChange={handleFileUpload}
          className="block w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 cursor-pointer focus:outline-none mb-4"
        />
        {uploading && <p className="text-indigo-600 font-medium">Uploading and generating quiz...</p>}
        {error && <p className="text-red-600 font-medium">{error}</p>}
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
    <div className="w-full max-w-2xl">
      {renderUploadSection()}
      {!quizCompleted ? (
        <div className="bg-white rounded-2xl shadow-xl p-8">
          <div className="mb-8">
            <div className="flex justify-between items-center mb-4">
              <span className="text-sm font-medium text-gray-500">
                Question {currentQuestion + 1} of {questionsState.length}
              </span>
              <span className="px-3 py-1 bg-indigo-100 text-indigo-800 rounded-full text-sm font-medium">
                {Math.round(((currentQuestion + 1) / questionsState.length) * 100)}%
              </span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div
                className="bg-indigo-600 h-2 rounded-full transition-all duration-300"
                style={{ width: `${((currentQuestion + 1) / questionsState.length) * 100}%` }}
              ></div>
            </div>
          </div>

          <h2 className="text-2xl font-bold text-gray-800 mb-6">
            {questionsState[currentQuestion].question}
          </h2>

          <div className="space-y-3">
            {questionsState[currentQuestion].options.map((option, index) => (
              <div
                key={index}
                className={`p-4 mb-3 rounded-lg transition-all duration-300 ${
                  selectedAnswer === index
                    ? "border-2 border-indigo-500 bg-indigo-50"
                    : "border-2 border-gray-200 hover:bg-gray-50 cursor-pointer"
                }`}
                onClick={() => handleAnswerSelect(index)}
              >
                {option}
              </div>
            ))}
          </div>

          {selectedAnswer !== null && (
            <button
              onClick={handleNext}
              className="mt-6 w-full bg-indigo-600 text-white py-3 px-6 rounded-lg font-semibold hover:bg-indigo-700 transition-colors duration-300 flex items-center justify-center"
            >
              {currentQuestion === questionsState.length - 1 ? "Finish Quiz" : "Next Question"}
              <ArrowRight className="ml-2 w-5 h-5" />
            </button>
          )}
        </div>
      ) : (
        <div className="bg-white rounded-2xl shadow-xl p-8 text-center">
          <h2 className="text-3xl font-bold text-gray-800">Quiz Completed!</h2>

          {/* Display Score */}
          <div className="mt-4 text-xl font-semibold">
            <p>
              Score: {calculateScore().score} / {calculateScore().total} (
              {calculateScore().percentage}%)
            </p>
          </div>

          {/* Show Correct Answers & Explanations */}
          <div className="mt-6 text-left">
            {quizResults.map((result, index) => (
              <div key={index} className="p-4 mb-3 border rounded-lg bg-gray-50">
                <p className="font-bold">{questionsState[index].question}</p>
                <p
                  className={`font-medium mt-2 ${
                    result.isCorrect ? "text-green-600" : "text-red-600"
                  }`}
                >
                  Your Answer: {questionsState[index].options[result.userAnswer]}
                </p>
                {!result.isCorrect && (
                  <p className="text-blue-600">
                    Correct Answer: {questionsState[index].options[result.correctAnswer]}
                  </p>
                )}
                <p className="text-gray-700 mt-2">{questionsState[index].explanation}</p>
              </div>
            ))}
          </div>

          {/* Restart Quiz Button */}
          <button
            onClick={() => {
              setQuizCompleted(false);
              setCurrentQuestion(0);
              setSelectedAnswer(null);
              setQuizResults([]);
            }}
            className="mt-6 bg-indigo-600 text-white py-3 px-6 rounded-lg font-semibold hover:bg-indigo-700 transition-colors duration-300 flex items-center justify-center"
          >
            <RefreshCw className="mr-2 w-5 h-5" /> Restart Quiz
          </button>
        </div>
      )}
    </div>
  </div>
  );
}

export default App;
