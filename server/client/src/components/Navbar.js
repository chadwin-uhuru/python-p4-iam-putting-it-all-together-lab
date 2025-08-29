import React from "react";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";

function Navbar({ user, setUser }) {
  const navigate = useNavigate();

  const handleLogout = () => {
    axios.delete("/logout", { withCredentials: true })
      .then(() => {
        setUser(null);
        navigate("/login");
      });
  };

  return (
    <nav>
      <Link to="/recipes">Recipes</Link>
      {user ? (
        <>
          <span>Welcome, {user.username}</span>
          <button onClick={handleLogout}>Logout</button>
        </>
      ) : (
        <>
          <Link to="/signup">Sign Up</Link>
          <Link to="/login">Login</Link>
        </>
      )}
    </nav>
  );
}

export default Navbar;
