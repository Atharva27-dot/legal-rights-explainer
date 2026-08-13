import {
  FaUser,
  FaBalanceScale,
} from "react-icons/fa";

export default function ChatBubble({ message }) {

  const isUser = message.type === "user";

  return (

    <div
      className={`flex ${
        isUser ? "justify-end" : "justify-start"
      }`}
    >

      <div
        className={`flex gap-4 max-w-5xl ${
          isUser ? "flex-row-reverse" : ""
        }`}
      >

        {/* Avatar */}

        <div
          className={`w-12 h-12 rounded-2xl flex items-center justify-center shadow-md flex-shrink-0 ${
            isUser
              ? "bg-gradient-to-r from-blue-900 to-indigo-700"
              : "bg-gradient-to-r from-emerald-600 to-teal-500"
          }`}
        >

          {isUser ? (
            <FaUser className="text-white text-lg" />
          ) : (
            <FaBalanceScale className="text-white text-lg" />
          )}

        </div>

        {/* Message */}

        <div
          className={`rounded-3xl shadow-lg border p-6 ${
            isUser
              ? "bg-blue-900 text-white border-blue-900"
              : "bg-white border-slate-200"
          }`}
        >

          {/* Sender */}

          <p
            className={`font-bold mb-3 ${
              isUser
                ? "text-blue-100"
                : "text-blue-900"
            }`}
          >

            {isUser
              ? "You"
              : "AI Legal Assistant"}

          </p>

          {/* Text */}

          <div
            className={`whitespace-pre-wrap leading-8 ${
              isUser
                ? "text-white"
                : "text-slate-700"
            }`}
          >

            {message.text}

          </div>

        </div>

      </div>

    </div>

  );

}