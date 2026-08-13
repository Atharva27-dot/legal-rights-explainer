import {
  FaBalanceScale,
  FaArrowRight,
  FaQuestionCircle,
} from "react-icons/fa";

const suggestions = [
  {
    icon: "🛒",
    text: "Who is a consumer?",
  },
  {
    icon: "💰",
    text: "Can I get a refund for a defective product?",
  },
  {
    icon: "⚖️",
    text: "How do I file a consumer complaint?",
  },
  {
    icon: "📦",
    text: "What are my consumer rights?",
  },
];

export default function WelcomeScreen({ setQuestion }) {
  return (
    <div className="bg-white rounded-3xl shadow-xl border border-slate-200 overflow-hidden">

      {/* Hero */}

      <div className="bg-gradient-to-r from-blue-900 via-indigo-700 to-blue-600 text-white p-12">

        <div className="flex items-center gap-5">

          <div className="w-20 h-20 rounded-3xl bg-white/20 flex items-center justify-center">

            <FaBalanceScale className="text-4xl" />

          </div>

          <div>

            <h1 className="text-4xl font-bold">

              Legal Rights Explainer

            </h1>

            <p className="mt-3 text-blue-100 text-lg">

              AI-powered legal assistance for Indian citizens.

            </p>

          </div>

        </div>

      </div>

      {/* Description */}

      <div className="p-10">

        <div className="flex items-center gap-3 mb-6">

          <FaQuestionCircle className="text-blue-700 text-xl" />

          <h2 className="text-2xl font-bold text-slate-800">

            Ask Legal Questions in Plain Language

          </h2>

        </div>

        <p className="text-slate-600 leading-8">

          This AI assistant retrieves relevant legal provisions from Indian
          laws and explains them in simple language. It also provides
          supporting legal sources, confidence levels, and guidance on the
          next steps.

        </p>

        {/* Suggestions */}

        <div className="mt-10">

          <h3 className="text-xl font-semibold mb-5">

            Try asking one of these questions

          </h3>

          <div className="grid md:grid-cols-2 gap-5">

            {suggestions.map((item, index) => (

              <button
                key={index}
                onClick={() => setQuestion(item.text)}
                className="group border border-slate-200 rounded-2xl p-5 text-left hover:border-blue-700 hover:bg-blue-50 transition-all duration-300 shadow-sm hover:shadow-lg"
              >

                <div className="flex items-center justify-between">

                  <div className="flex items-center gap-4">

                    <span className="text-3xl">

                      {item.icon}

                    </span>

                    <span className="font-medium text-slate-700">

                      {item.text}

                    </span>

                  </div>

                  <FaArrowRight className="text-blue-700 opacity-0 group-hover:opacity-100 transition" />

                </div>

              </button>

            ))}

          </div>

        </div>

        {/* Footer */}

        <div className="mt-10 rounded-2xl bg-slate-100 p-6 border border-slate-200">

          <h3 className="font-semibold text-slate-800">

            💡 Tip

          </h3>

          <p className="mt-2 text-slate-600">

            Ask complete questions for better results.
            Example:
            <strong>
              {" "}
              "Can I get a refund for a defective product purchased online?"
            </strong>

          </p>

        </div>

      </div>

    </div>
  );
}