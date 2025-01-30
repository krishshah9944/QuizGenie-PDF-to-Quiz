export interface Question {
  id: number;
  question: string;
  options: string[];
  correctAnswer: number;
  explanation: string;
}

export interface QuizResult {
  questionId: number;
  userAnswer: number;
  isCorrect: boolean;
}

export const questions: Question[] = [
  {
    id: 1,
    question: "What is the capital of France?",
    options: ["London", "Berlin", "Paris", "Madrid"],
    correctAnswer: 2,
    explanation: "Paris is the capital and largest city of France, known for its iconic Eiffel Tower and rich cultural heritage."
  },
  {
    id: 2,
    question: "Which planet is known as the Red Planet?",
    options: ["Venus", "Mars", "Jupiter", "Saturn"],
    correctAnswer: 1,
    explanation: "Mars appears red because of iron oxide (rust) on its surface, hence the nickname 'Red Planet'."
  },
  {
    id: 3,
    question: "Who painted the Mona Lisa?",
    options: ["Vincent van Gogh", "Pablo Picasso", "Leonardo da Vinci", "Michelangelo"],
    correctAnswer: 2,
    explanation: "The Mona Lisa was painted by Leonardo da Vinci in the early 16th century and is now displayed at the Louvre Museum in Paris."
  }
];