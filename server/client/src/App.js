import React, { useEffect, useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import axios from "axios";
import Signup from "./components/Signup";
import Login from "./components/Login";
import Recipes from "./components/Recipes";
import RecipeForm from "./components/RecipeForm";
import Navbar from "./components/Navbar";

function App() {
  const [user, setUser] = useState(null);

  // Auto-login on refresh
  useEffect(() => {
    axios.get("/check_session", { withCredentials: true })
      .then(res => setUser(res.data))
      .catch(() => setUser(null));
  }, []);

  return (
    <Router>
      <Navbar user={user} setUser={setUser} />
      <Routes>
        <Route path="/signup" element={<Signup setUser={setUser} />} />
        <Route path="/login" element={<Login setUser={setUser} />} />
        <Route path="/recipes" element={<Recipes />} />
        <Route path="/new-recipe" element={<RecipeForm user={user} />} />
      </Routes>
    </Router>
  );
}

export default App;
