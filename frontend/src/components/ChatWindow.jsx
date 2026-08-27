import ChatBubble from "./ChatBubble";
import AnswerCard from "./AnswerCard";
import SourceCard from "./SourceCard";
import StatsCard from "./StatsCard";

export default function ChatWindow({ messages }) {
  return (
    <div className="space-y-6">
      {messages.map((message, index) => (
        <div key={index}>

          {/* Show the citizen's question as a chat bubble.
              The AI answer is rendered only once below, avoiding
              the previous duplicated response. */}
          {message.type === "user" && (
            <ChatBubble message={message} />
          )}

          {message.type === "ai" && (
            <div className="space-y-5">

              <AnswerCard answer={message.answer} />

              <SourceCard sources={message.sources} />

              <StatsCard
                confidence={message.confidence}
                retrieval_time={message.retrieval_time}
                llm_time={message.llm_time}
                total_time={message.total_time}
              />

            </div>
          )}

        </div>
      ))}
    </div>
  );
}
