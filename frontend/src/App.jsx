import { BrowserRouter, Routes, Route } from "react-router-dom";

import Home from "./pages/Home";
import ComplaintGenerator from "./pages/ComplaintGenerator";
import RightsGuide from "./pages/RightsGuide";
import SavedReports from "./pages/SavedReports";
import About from "./pages/About";
import MyCases from "./pages/MyCases";

function App() {

  return (

    <BrowserRouter>

      <Routes>

        <Route path="/" element={<Home />} />

        <Route
          path="/complaint"
          element={<ComplaintGenerator />}
        />

        <Route
          path="/rights"
          element={<RightsGuide />}
        />

        <Route
          path="/reports"
          element={<SavedReports />}
        />

        <Route
          path="/about"
          element={<About />}
        />

        <Route path="/my-cases" element={<MyCases />} />

      </Routes>

      

    </BrowserRouter>

  );

}

export default App;