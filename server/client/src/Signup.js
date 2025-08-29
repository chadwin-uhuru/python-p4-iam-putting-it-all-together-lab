import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

function Signup({ setUser }) {
  const [form, setForm] = useState({ username: "", password: "", bio: "", image_url: "" });
  const [errors, setErrors] = useState([]);
  const navigate = useNavigate();

  const handleChange = e => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = e => {
    e.preventDefault();
    axios.post("/signup", form, { withCredentials: true })
      .then(res => {
        setUser(res.data);
        navigate("/recipes");
      })
      .catch(err => setErrors(err.response.data.errors || ["Signup failed"]));
  };

  return (
    <div>
      <h2>Sign Up</h2>
      {errors.map((e, i) => <p key={i} style={{ color: "red" }}>{e}</p>)}
      <form onSubmit={handleSubmit}>
        <input name="username" placeholder="Username" onChange={handleChange} />
        <input name="password" type="password" placeholder="Password" onChange={handleChange} />
        <input name="bio" placeholder="Bio" onChange={handleChange} />
        <input name="image_url" placeholder="Image URL" onChange={handleChange} />
        <button type="submit">Sign Up</button>
      </form>
    </div>
  );
}

export default Signup;
