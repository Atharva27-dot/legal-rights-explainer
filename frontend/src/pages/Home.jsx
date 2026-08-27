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

      <main className="max-w-[1500px] mx-auto py-8 px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-[270px_minmax(0,1fr)] gap-6 xl:gap-8 items-start">

          <aside className="lg:sticky lg:top-6">
            <Sidebar />
          </aside>

          <section className="min-w-0 space-y-6">

            {/* Page heading */}
            <div className="bg-white border border-slate-200 rounded-3xl shadow-sm px-6 py-5">
              <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">

                <div>
                  <p className="text-sm font-semibold text-indigo-700">
                    LEGAL ASSISTANT
                  </p>

                  <h1 className="text-2xl sm:text-3xl font-bold text-slate-900 mt-1">
                    Understand your legal rights
                  </h1>

                  <p className="text-slate-500 mt-2">
                    Ask a legal question in simple language and get an
                    explanation grounded in the uploaded legal documents.
                  </p>
                </div>

                <div className="flex items-center gap-2 self-start sm:self-center bg-emerald-50 border border-emerald-200 rounded-full px-3 py-2">
                  <span className="w-2.5 h-2.5 rounded-full bg-emerald-500" />
                  <span className="text-xs font-semibold text-emerald-700">
                    AI Online
                  </span>
                </div>

              </div>
            </div>

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

          </section>
        </div>
      </main>
    </div>
  );
}
