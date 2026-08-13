import { useEffect, useMemo, useState } from "react";
import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import CaseCard from "../components/CaseCard";
import { getCases } from "../services/api";

export default function MyCases() {
  const [cases, setCases] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");

  useEffect(() => {
    loadCases();
  }, []);

  const loadCases = async () => {
    try {
      setLoading(true);

      const response = await getCases();

      setCases(response.cases || []);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const filteredCases = useMemo(() => {
    const keyword = search.toLowerCase();

    return cases.filter((item) => {
      return (
        item.case_id.toLowerCase().includes(keyword) ||
        item.citizen_name.toLowerCase().includes(keyword) ||
        item.category.toLowerCase().includes(keyword)
      );
    });
  }, [cases, search]);

  return (
    <div className="min-h-screen bg-slate-100">

      <Navbar />

      <main className="max-w-7xl mx-auto py-10 px-6">

        <div className="grid grid-cols-12 gap-8">

          {/* Sidebar */}

          <div className="col-span-3">

            <Sidebar />

          </div>

          {/* Content */}

          <div className="col-span-9 space-y-8">

            <div className="bg-gradient-to-r from-blue-900 via-indigo-700 to-blue-600 rounded-3xl shadow-xl p-10 text-white">

              <h1 className="text-4xl font-bold">

                My Legal Cases

              </h1>

              <p className="mt-3 text-blue-100 text-lg">

                View and manage all saved legal complaints.

              </p>

            </div>

            <input
              type="text"
              placeholder="Search by Case ID, Name or Category..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full rounded-xl border border-slate-300 p-4"
            />

            {loading ? (

              <div className="text-center py-20">

                <h2 className="text-xl font-semibold">

                  Loading Cases...

                </h2>

              </div>

            ) : filteredCases.length === 0 ? (

              <div className="bg-white rounded-3xl shadow-xl p-20 text-center">

                <div className="text-6xl">

                  📂

                </div>

                <h2 className="mt-5 text-3xl font-bold">

                  No Saved Cases

                </h2>

                <p className="mt-3 text-slate-500">

                  Generate and save a complaint to see it here.

                </p>

              </div>

            ) : (

              <div className="grid gap-6">

                {filteredCases.map((item) => (

                  <CaseCard
                    key={item.case_id}
                    caseItem={item}
                    refreshCases={loadCases}
                  />

                ))}

              </div>

            )}

          </div>

        </div>

      </main>

    </div>
  );
}