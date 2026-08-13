import { useState } from "react";

import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import ChatInput from "../components/ChatInput";
import ChatWindow from "../components/ChatWindow";
import Loader from "../components/Loader";
import WelcomeScreen from "../components/WelcomeScreen";

import { askQuestion } from "../services/api";

export default function Home() {
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState([]);

  const handleAsk = async () => {
    if (!question.trim()) return;

    const userMessage = {
      type: "user",
      text: question,
    };

    setMessages((prev) => [...prev, userMessage]);

    setLoading(true);

    try {
      const response = await askQuestion(question);

      const aiMessage = {
        type: "ai",
        text: response.answer,
        answer: response.answer,
        sources: response.sources,
        confidence: response.confidence,
        retrieval_time: response.retrieval_time,
        llm_time: response.llm_time,
        total_time: response.total_time,
      };

      setMessages((prev) => [...prev, aiMessage]);

      setQuestion("");
    } catch (error) {
      console.error(error);

      if (error.response) {
        alert(`Backend Error: ${error.response.status}`);
      } else if (error.request) {
        alert("Cannot connect to backend. Is FastAPI running?");
      } else {
        alert(error.message);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-100">
      <Navbar />

      <main className="max-w-7xl mx-auto py-10 px-6">
        <div className="grid grid-cols-12 gap-8">
          {/* Sidebar */}
          <div className="col-span-3">
            <Sidebar />
          </div>

          {/* Main Content */}
          <div className="col-span-9 space-y-6">
            <ChatInput
              question={question}
              setQuestion={setQuestion}
              loading={loading}
              handleAsk={handleAsk}
            />

            {loading && <Loader />}

            {!loading && messages.length === 0 && (
              <WelcomeScreen setQuestion={setQuestion} />
            )}

            {!loading && messages.length > 0 && (
              <ChatWindow messages={messages} />
            )}
          </div>
        </div>
      </main>
    </div>
  );
}