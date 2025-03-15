import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import CreateSocialMediaAccount from "./components/CreateSocialMediaAccountModal";

const App: React.FC = () => {
  return (
    <Router>
  
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path='/create-account/:platform' element={<CreateSocialMediaAccount/>}/>
       
      </Routes>
    </Router>
  );
};

export default App;
