import { useState } from "react";
import AppShell from "../components/AppShell";
import ChatInput from "../components/ChatInput";
import ChatWindow from "../components/ChatWindow";
import Loader from "../components/Loader";
import WelcomeScreen from "../components/WelcomeScreen";
import { askQuestion } from "../services/api";
import { Sparkles, ShieldCheck, HelpCircle } from "lucide-react";
import toast from "react-hot-toast";

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
        toast.error(`Backend Error: ${error.response.status}`);
      } else if (error.request) {
        toast.error("Cannot connect to legal assistant backend. Is FastAPI running on port 8000?");
      } else {
        toast.error(error.message || "An unexpected error occurred.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <AppShell>
      <div className="space-y-6">
        {/* Page Top Heading Banner */}
        <div className="bg-white border border-slate-200/80 rounded-2xl p-5 sm:p-6 shadow-xs flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 text-xs font-bold text-indigo-600 tracking-wider uppercase mb-1">
              <Sparkles className="w-3.5 h-3.5" />
              <span>Legal RAG Assistant</span>
            </div>
            <h1 className="text-xl sm:text-2xl font-black text-slate-900 tracking-tight">
              Plain-Language Legal Rights Assistant
            </h1>
            <p className="text-xs sm:text-sm text-slate-500 mt-1">
              Ask any question to retrieve statutory provisions, understand citizen remedies, and view confidence metrics.
            </p>
          </div>

          <div className="flex items-center gap-2 bg-emerald-50 border border-emerald-200 rounded-full px-3 py-1.5 self-start sm:self-center">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-ping" />
            <span className="text-xs font-bold text-emerald-700">RAG Engine Ready</span>
          </div>
        </div>

        {/* Question Input Box */}
        <ChatInput
          question={question}
          setQuestion={setQuestion}
          loading={loading}
          handleAsk={handleAsk}
        />

        {/* Loader State */}
        {loading && <Loader />}

        {/* Welcome Screen when idle */}
        {!loading && messages.length === 0 && (
          <WelcomeScreen setQuestion={setQuestion} />
        )}

        {/* Messages / AI Response Stream */}
        {!loading && messages.length > 0 && (
          <ChatWindow messages={messages} />
        )}
      </div>
    </AppShell>
  );
}
