import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";

export default function About() {
  return (
    <div className="min-h-screen bg-slate-100">
      <Navbar />

      <main className="max-w-7xl mx-auto py-10 px-6">
        <div className="grid grid-cols-12 gap-8">

          <div className="col-span-3">
            <Sidebar />
          </div>

          <div className="col-span-9">
            <div className="bg-white rounded-xl shadow-lg p-8">
              <h1 className="text-3xl font-bold text-blue-900">
                About
              </h1>

              <p className="mt-4 text-gray-600">
                AI-powered Legal Rights Explainer for Indian Citizens.
              </p>
            </div>
          </div>

        </div>
      </main>
    </div>
  );
}