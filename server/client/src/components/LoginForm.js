import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

function LoginForm({ setUser }) {
  const [form, setForm] = useState({ username: "", password: "" });
  const [errors, setErrors] = useState([]); // ✅ Make sure this is an array
  const navigate = useNavigate();

  const handleChange = e => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = e => {
    e.preventDefault();
    axios.post("/login", form, { withCredentials: true })
      .then(res => {
        setUser(res.data); // set user in App state
        navigate("/recipes"); // redirect after login
      })
      .catch(err => {
        // Ensure errors is always an array
        if (err.response && err.response.data && err.response.data.errors) {
          setErrors(err.response.data.errors);
        } else {
          setErrors([err.response?.data?.error || "Login failed"]);
        }
      });
  };

  return (
    <div>
      <h2>Login</h2>
      {errors.length > 0 && errors.map((e, i) => (
        <p key={i} style={{ color: "red" }}>{e}</p>
      ))}
      <form onSubmit={handleSubmit}>
        <input name="username" placeholder="Username" onChange={handleChange} />
        <input name="password" type="password" placeholder="Password" onChange={handleChange} />
        <button type="submit">Login</button>
      </form>
    </div>
  );
}

export default LoginForm;
