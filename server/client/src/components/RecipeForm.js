import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

function RecipeForm({ user }) {
  const [form, setForm] = useState({ title: "", instructions: "", minutes_to_complete: "" });
  const [errors, setErrors] = useState([]);
  const navigate = useNavigate();

  if (!user) {
    return <p>You must be logged in to create a recipe.</p>;
  }

  const handleChange = e => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = e => {
    e.preventDefault();
    axios.post("/recipes", form, { withCredentials: true })
      .then(res => {
        navigate("/recipes");
      })
      .catch(err => setErrors(err.response.data.errors || ["Failed to create recipe"]));
  };

  return (
    <div>
      <h2>Create Recipe</h2>
      {errors.map((e, i) => <p key={i} style={{ color: "red" }}>{e}</p>)}
      <form onSubmit={handleSubmit}>
        <input name="title" placeholder="Title" onChange={handleChange} />
        <textarea name="instructions" placeholder="Instructions" onChange={handleChange} />
        <input name="minutes_to_complete" placeholder="Minutes to Complete" type="number" onChange={handleChange} />
        <button type="submit">Create</button>
      </form>
    </div>
  );
}

export default RecipeForm;
