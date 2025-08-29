import React, { useState } from "react";
import { signup } from "../api";

function SignupForm({ setUser }) {
  const [formData, setFormData] = useState({
    username: "",
    password: "",
    image_url: "",
    bio: ""
  });
  const [errors, setErrors] = useState([]);

  const handleChange = (e) => {
    setFormData({...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const res = await signup(formData);
    if (res.errors) setErrors(res.errors);
    else setUser(res);
  };

  return (
    <div>
      <h2>Sign Up</h2>
      <form onSubmit={handleSubmit}>
        <input name="username" placeholder="Username" onChange={handleChange} />
        <input type="password" name="password" placeholder="Password" onChange={handleChange} />
        <input name="image_url" placeholder="Image URL" onChange={handleChange} />
        <input name="bio" placeholder="Bio" onChange={handleChange} />
        <button type="submit">Sign Up</button>
      </form>
      {errors.map((e, i) => <p key={i} style={{color:"red"}}>{e}</p>)}
    </div>
  );
}

export default SignupForm;
