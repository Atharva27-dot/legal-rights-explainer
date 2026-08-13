import {
  FaCheckCircle,
  FaClock,
  FaRobot,
  FaDatabase,
} from "react-icons/fa";

export default function StatsCard({
  confidence,
  retrieval_time,
  llm_time,
  total_time,
}) {
  if (!confidence) return null;

  const confidenceColor = {
    High: "text-green-600",
    Medium: "text-yellow-500",
    Low: "text-red-500",
  };

  const cards = [
    {
      icon: <FaCheckCircle className={`text-3xl ${confidenceColor[confidence] || "text-green-600"}`} />,
      title: "Confidence",
      value: confidence,
      bg: "from-green-50 to-green-100",
    },
    {
      icon: <FaDatabase className="text-3xl text-blue-700" />,
      title: "Retrieval",
      value: `${retrieval_time} sec`,
      bg: "from-blue-50 to-blue-100",
    },
    {
      icon: <FaRobot className="text-3xl text-purple-700" />,
      title: "AI Generation",
      value: `${llm_time} sec`,
      bg: "from-purple-50 to-purple-100",
    },
    {
      icon: <FaClock className="text-3xl text-orange-600" />,
      title: "Total Time",
      value: `${total_time} sec`,
      bg: "from-orange-50 to-orange-100",
    },
  ];

  return (
    <div className="mt-8">

      <h2 className="text-2xl font-bold text-slate-800 mb-5">
        📊 AI Performance
      </h2>

      <div className="grid md:grid-cols-4 gap-5">

        {cards.map((card, index) => (

          <div
            key={index}
            className={`rounded-3xl bg-gradient-to-br ${card.bg} border border-slate-200 shadow-lg p-6 hover:shadow-xl transition-all duration-300 hover:-translate-y-1`}
          >

            <div className="mb-5">
              {card.icon}
            </div>

            <h3 className="text-slate-600 font-medium">
              {card.title}
            </h3>

            <p className="mt-2 text-2xl font-bold text-slate-800">
              {card.value}
            </p>

          </div>

        ))}

      </div>

    </div>
  );
}